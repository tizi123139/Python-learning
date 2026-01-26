# **FastAPI**

FastAPI 是一个现代、快速（高性能）的 Web 框架，用于使用基于标准 Python 类型提示的 Python 构建 API。

---

### 创建

```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### 交互式 API 文档

现在访问 http://127.0.0.1:8000/docs



### `async` 和 `await`

当某个操作需要等待才能返回结果，并且该操作支持这些新的 Python 功能时，可以像这样编写代码：

```
burgers = await get_burgers(2)
```

这里的关键是 `await`。它告诉 Python 必须等待 ⏸ `get_burgers(2)` 完成其工作 🕙，然后才能将结果存储在 `burgers` 中。通过这样做，Python 将知道它可以在此期间去做其他事情 🔀 ⏯（例如接收另一个请求）。

为了使 `await` 生效，它必须包含在一个支持这种异步的函数中。为此，只需使用 `async def` 声明它即可：

```
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
```



## 路径参数

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

### 带类型的路径参数

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```



## 查询参数

查询参数是以 `?` 符号分隔的一组键值对，后面跟着 URL，并用 `&` 字符分隔。

http://127.0.0.1:8000/items/?skip=0&limit=10

查询参数是

- `skip`：值为 `0`
- `limit`：值为 `10`

### 可选参数

可以通过将默认值设置为 `None` 来声明可选的查询参数

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

### 字符串验证



## 请求体

**请求体**是客户端发送给你的 API 的数据。**响应体**是你的 API 发送给客户端的数据。

- 导入 Pydantic 的 BaseModel
- 创建你的数据模型
- 将其声明为一个参数

```
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```



[学习 - FastAPI - FastAPI 框架](https://fastapi.org.cn/learn/)

---

# **SQLAlchemy**

---

SQLAlchemy 是一个流行的 SQL 工具包和**对象关系映射器**。它用**Python**编写，为应用程序开发人员提供了 SQL 的全部功能和灵活性。

很多人把SQLAlchemy等同于一款ORM（对象关系映射）工具。这没错，但它的核心价值远不止于此。你可以把它理解为一个**强大的“数据库连接与查询构建工厂”**。

想象一下餐厅的后厨：

\- 🛠️ **引擎（Engine）**：餐厅的“中央厨房”。它是数据库连接的工厂和连接池的持有者。你配置好一次（数据库地址、连接参数、池大小），整个应用都从这里“取用”连接。它是全局的、重量级的。

\- 🧾 **会话（Session）**：厨师手中的“订单篮”。一个Session代表一个独立的数据库操作“工作单元”。它从Engine获取一个物理连接，管理一系列相关的增删改查，并在完成后“归还”连接。它是局部的、轻量级的，**并且绝对不应该跨请求共享**。

\- 🍝 **ORM（Declarative Base）**：标准化的“菜谱”。它定义了数据模型（表结构）和业务对象（Python类）的映射关系，让你能用面向对象的方式操作数据库。

**关键结论：高性能存取的核心，在于正确管理Engine和Session的生命周期。** Engine通常应用启动时创建，关闭时销毁。而Session必须**“即用即创，用完即关”**，且每个请求独立。

---

## 连接到数据库

```
engine = create_engine("mysql://user:pwd@localhost/college",echo = True)
```

**echo 标志** 是设置 SQLAlchemy 日志记录的快捷方式，它通过 Python 的标准日志记录模块完成。

create_engine() 函数返回一个 **Engine 对象**。Engine 类的一些重要方法是 

| Sr.No. |                          方法与说明                          |
| :----: | :----------------------------------------------------------: |
|   1    |                  **connect()**返回连接对象                   |
|   2    |                **execute()**执行 SQL 语句构造                |
|   3    | **begin()**返回一个上下文管理器，该管理器提供已建立事务的连接。操作成功后，事务提交，否则回滚 |
|   4    |              **dispose()**处理引擎使用的连接池               |
|   5    |           **driver()**引擎使用的方言的驱动程序名称           |
|   6    |       **table_names()**返回数据库中所有可用表名的列表        |
|   7    |          **transaction()**在事务边界内执行给定函数           |

## 声明映射

基类在声明系统中存储类和映射表的目录。这被称为声明基类。通常，在通常导入的模块中只有一个此基类的实例。declarative_base() 函数用于创建基类。此函数在 sqlalchemy.ext.declarative 模块中定义。

```
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

一旦声明了基类，就可以根据它定义任意数量的映射类。

```
class Customers(Base):
   __tablename__ = 'customers'
   
   id = Column(Integer, primary_key = True)
   name = Column(String)
   address = Column(String)
   email = Column(String)
```

Declarative 中的类必须具有 **__tablename__** 属性，以及至少一个作为主键一部分的 **Column**。

## 创建会话

会话对象是数据库的句柄。会话类使用 sessionmaker() 定义 - 一个可配置的会话工厂方法，它绑定到先前创建的引擎对象。

```
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
```

## 构建 begin / commit / rollback 代码块

```
with Session(engine) as session:
    session.begin()
    try:
        session.add(some_object)
        session.add(some_other_object)
    except:
        session.rollback()
        raise
    else:
        session.commit()
```

## FastAPI + SQLite + SQLAlchemy操作数据库

### 第一步：创建核心引擎与模型

```
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 定义数据库文件路径
SQLALCHEMY_DATABASE_URL = f"sqlite:///./test.db"

# 创建引擎 (核心)
# `connect_args={"check_same_thread": False}` 对于SQLite多线程是必须的
# `echo=True` 开发时开启，可以查看生成的SQL，生产环境请关闭
# `pool_pre_ping=True` 连接池取出连接前进行健康检查，避免使用失效连接
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False, # 生产环境设为False
    pool_pre_ping=True,
    pool_size=5, # 连接池大小
    max_overflow=10 # 允许超出pool_size的临时连接数
)

# 创建会话工厂，绑定到引擎
# `autocommit=False, autoflush=False` 是推荐设置，便于事务控制
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明性基类，所有模型类都将继承自此
Base = declarative_base()
```

### 第二步：定义数据模型与依赖注入

```
# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)

# 创建表（通常在应用启动时调用一次）
# Base.metadata.create_all(bind=engine)

# dependencies.py
from database import SessionLocal
from fastapi import Depends
from typing import Generator

def get_db() -> Generator:
    """
    数据库会话依赖项。
    每个请求获取一个独立Session，请求结束后确保关闭。
    """
    db = SessionLocal()
    try:
        yield db # 将db注入到路由函数中
    finally:
        db.close() # 无论请求成功与否，最终都会关闭会话
```

### 第三步：在路由中实现CRUD

```
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from models import User
from dependencies import get_db

app = FastAPI()

# Pydantic模型，用于请求/响应验证
class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True # 允许从ORM对象转换

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # 创建ORM对象
    db_user = User(username=user.username, email=user.email)
    # 添加到会话
    db.add(db_user)
    # 提交事务
    db.commit()
    # 刷新，使对象获得数据库生成的ID等数据
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
```





[SQLAlchemy ORM — SQLAlchemy 2.0 文档 - SQLAlchemy 中文](https://docs.sqlalchemy.org.cn/en/20/orm/index.html)

[SQLAlchemy 教程 | SQLAlchemy从入门到精通 | w3schools 中文网](https://www.w3ccoo.com/sqlalchemy/index.html)



