# 导包
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from utils.log import Logger
from utils.common import data_preprocessing
from xgboost import XGBRegressor, XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib


plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 15


# 1. 定义电力负荷模型类, 配置日志, 获取数据源.
class PowerLoadModel:
    # 1.1 初始化属性信息.
    def __init__(self):
        # 1.2 拼接日志文件名.
        logfile_name = 'train_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 1.3 创建日志对象.
        self.logfile = Logger('../', logfile_name).get_logger()
        # 测试写一条日志.
        self.logfile.info('开始创建 电力负荷模型类的 对象了')
        # 1.4 获取数据源.
        self.data_source = data_preprocessing()


# 2. 查看数据的整体分布情况.
def ana_data(data):     # analysis: 分析
    """
    1.查看数据整体情况
    2.负荷整体的分布情况
    3.各个小时的平均负荷趋势，看一下负荷在一天中的变化情况
    4.各个月份的平均负荷趋势，看一下负荷在一年中的变化情况
    5.工作日与周末的平均负荷情况，看一下工作日的负荷与周末的负荷是否有区别
    :param data: 数据源
    :return:
    """
    # 0. 为了防止会修改源数据, 我们做一次拷贝.
    ana_data = data.copy()

    # 1. 查看数据整体情况
    ana_data.info()

    # 2. 负荷整体的分布情况, 直方图.
    # 2.1 创建画布.
    fig = plt.figure(figsize=(20, 40))
    # 2.2 添加子图.
    ax1 = fig.add_subplot(411)
    ax1.hist(ana_data['power_load'], bins=100)      # 负荷, 直方图, 100个区间
    ax1.set_title('负荷整体分布情况')
    ax1.set_xlabel('负荷')

    # 3.各个小时的平均负荷趋势，看一下负荷在一天中的变化情况
    # 3.1 新增1列, 充当小时.
    ana_data['hour'] = ana_data['time'].str[11:13]
    # 3.2 根据小时分组, 计算平均值.
    hour_load_mean = ana_data.groupby('hour', as_index=False)['power_load'].mean()
    # print(hour_load_mean)       # [列1 hour, 列2 power_load 当前小时的平均负荷]

    # # 3.3 画出折线图.
    ax2 = fig.add_subplot(412)
    ax2.plot(hour_load_mean['hour'], hour_load_mean['power_load'])
    ax2.set_title('各个小时的平均负荷趋势')
    ax2.set_xlabel('小时')

    # 4.各个月份的平均负荷趋势，看一下负荷在一年中的变化情况
    ana_data['month'] = ana_data['time'].str[5:7]
    month_load_mean = ana_data.groupby('month', as_index=False)['power_load'].mean()
    ax3= fig.add_subplot(413)
    ax3.plot(month_load_mean['month'], month_load_mean['power_load'])
    ax3.set_title('各个月份的平均负荷趋势')
    # 5.工作日与周末的平均负荷情况，看一下工作日的负荷与周末的负荷是否有区别
    ana_data['weekday'] = ana_data['time'].apply(lambda x: pd.to_datetime(x).weekday())
    ana_data['is_holiday'] = ana_data['weekday'].apply(lambda x: 1 if x in [5,6] else 0)
    work_load_mean = ana_data[ana_data['is_holiday']==0].power_load.mean()
    holiday_load_mean = ana_data[ana_data['is_holiday']==1].power_load.mean()
    ax4 = fig.add_subplot(414)
    ax4.bar(['工作日','周末'],[work_load_mean,holiday_load_mean])
    ax4.set_title('工作日与周末的平均负荷情况')

    plt.savefig('../data/fig/负荷整体的分布情况.png')
    plt.show()


# 3. 特征工程.
def feature_engineering(data,logger):
    feature_data = data.copy()
    feature_data['hour']=feature_data['time'].str[11:13]
    feature_data['month']=feature_data['time'].str[5:7]
    hour_month_data = pd.get_dummies(feature_data[['hour','month']])
    feature_data = pd.concat([feature_data,hour_month_data],axis=1)

    load_1h_data = feature_data['power_load'].shift(1)
    load_2h_data = feature_data['power_load'].shift(2)
    load_3h_data = feature_data['power_load'].shift(3)
    load_shift_data = pd.concat([load_1h_data,load_2h_data,load_3h_data],axis=1)
    load_shift_data.columns = ['前1小时','前2小时','前3小时']
    feature_data = pd.concat([feature_data,load_shift_data],axis=1)

    feature_data['yesterday_time'] = feature_data['time'].apply(lambda x:(pd.to_datetime(x)-datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'))
    time_load_dict = feature_data.set_index('time')['power_load'].to_dict()
    feature_data['yesterday_load'] = feature_data['yesterday_time'].apply(lambda x:time_load_dict.get(x))
    feature_data = feature_data.dropna()
    feature_columns = list(hour_month_data.columns)+list(load_shift_data.columns)+['yesterday_load']
    #print(feature_columns)
    return feature_data,feature_columns
# 4. 模型训练, 评估.
def model_train(data,features,logger):
    x=data[features]
    y=data['power_load']
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=23)
   # param_dict={
   #     'n_estimators':[50,100,150,200],
   #     'max_depth':[3,5,6,7],
   #     'learning_rate':[0.01,0.1],
   # }
   # estimator=XGBRegressor()
   # gs=GridSearchCV(estimator=estimator,param_grid=param_dict,cv=5)
  #  gs.fit(x_train,y_train)
   # logger.info(gs.best_params_)

    estimator = XGBRegressor(n_estimators=100,max_depth=5,learning_rate=0.1)
    estimator.fit(x_train,y_train)
    y_pred = estimator.predict(x_test)

    joblib.dump(estimator,'../model/xgb_model.pkl')




# 5. 测试.
if __name__ == '__main__':
    # 4.1 创建电力负荷模型类的对象.
    pm = PowerLoadModel()
    # 4.2 打印数据源.
    # print(pm.data_source)

    # 4.3 查看数据分布.
    #ana_data(pm.data_source)
    feature_data,feature_columns = feature_engineering(pm.data_source,pm.logfile)
    model_train(feature_data,feature_columns,pm.logfile)

