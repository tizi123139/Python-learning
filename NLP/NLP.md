# NLP

## NLP 的核心任务

1. **文本理解**：让计算机理解人类语言的含义
2. **文本生成**：让计算机能够生成自然语言文本
3. **语言翻译**：实现不同语言之间的自动翻译
4. **情感分析**：识别文本中表达的情感倾向

## 文本预处理

### 文本清洗：净化原始文本数据

编码格式处理

特殊字符处理

| 字符类型 | 处理方法             | 应用场景     |
| :------- | :------------------- | :----------- |
| HTML标签 | 正则表达式移除       | 网页爬取文本 |
| 表情符号 | 移除或转换为文字描述 | 社交媒体分析 |
| 控制字符 | 过滤掉               | 所有文本处理 |
| 特殊标点 | 标准化处理           | 文本规范化   |

噪声数据去除

### 分词（Tokenization）：将文本分解为基本单元

#### 中文分词技术

中文没有明显的词边界，分词更为复杂。主要方法包括：

1. **基于词典的分词**：最大匹配法、最短路径法
2. **基于统计的分词**：HMM、CRF等序列标注方法
3. **基于深度学习的分词**：BiLSTM-CRF、BERT等模型

### 词性标注：理解词语的语法角色

#### 常见词性体系

不同语言和工具使用不同的词性标注体系：

**英文常用Penn Treebank标签集（部分）：**

- NN：名词
- VB：动词
- JJ：形容词
- RB：副词
- PRP：代词

**中文常用ICTCLAS标签集（部分）：**

- n：名词
- v：动词
- a：形容词
- d：副词
- r：代词

#### 自动词性标注方法

1. **基于规则的方法**：使用手工编写的规则进行标注
2. **基于统计的方法**：HMM、MaxEnt等模型
3. **基于深度学习的方法**：RNN、Transformer等神经网络

## RNN的不足

![img](https://i-blog.csdnimg.cn/blog_migrate/aef3622fd88b44bba45ad660e0db6142.png)

循环神经网络处理时间序列数据具有先天优势，通过反向传播和梯度下降算法达到了纠正错误的能力，但是在进行反向传播时也面临梯度消失或者梯度爆炸问题，这种问题表现在时间轴上。如果输入序列的长度很长，人们很难进行有效的参数更新。通常来说梯度爆炸更容易处理一些。梯度爆炸时我们可以设置一个梯度阈值，当梯度超过这个阈值的时候可以直接截取。

有三种方法应对梯度消失问题：

（1）合理的初始化权重值。初始化权重，使每个神经元尽可能不要取极大或极小值，以躲开梯度消失的区域。

（2）使用 ReLu 代替 sigmoid 和 tanh 作为激活函数。

（3）使用其他结构的RNNs，比如长短时记忆网络（LSTM）和 门控循环单元 （GRU），这是最流行的做法。



## 长短期记忆网络（LSTM）

LSTM（Long Short-Term Memory）是 RNN 的一种改进架构，专门设计来解决标准 RNN 的长期依赖问题。

LSTM 引入了三个门控机制和一个记忆单元：

| 组件     | 功能               |
| :------- | :----------------- |
| 输入门   | 控制新信息的流入   |
| 遗忘门   | 决定丢弃哪些旧信息 |
| 输出门   | 控制输出的信息量   |
| 记忆单元 | 保存长期状态       |

![img](https://i-blog.csdnimg.cn/blog_migrate/46936b67b417956e6863987b3c703040.png)

![img](https://i-blog.csdnimg.cn/blog_migrate/39edfccc691da3cffbd1ec2224dc7be7.png)

- Neural Network Layer：神经网络层，用于学习；

- Pointwise Operation：逐点运算操作，如逐点相乘、逐点相加、向量和等；

- Vector Transfer：向量转移，向量沿箭头方向移动；

- Concatenate：连接，将两个向量连接在一起；

- Copy：复制，将向量复制为两份。

LSTM网络能通过一种被称为门的结构对细胞状态进行删除或者添加信息。门能够有选择性的决定让哪些信息通过。门的结构为一个sigmoid层和一个点乘操作的组合，sigmoid层输出0到1之间的数，描述每个部分有多少量可以通过，0代表不允许任何量通过，1表示允许任何量通过，结构如下图所示：

![img](https://i-blog.csdnimg.cn/blog_migrate/234215e0908cdffbb1cecbf9c6be922f.png)

![img](https://i-blog.csdnimg.cn/blog_migrate/c4751f800ebe179a04d700633eac49af.png)

![img](https://i-blog.csdnimg.cn/blog_migrate/605afb9ac22df3ff0f778845d16b4517.gif)

**遗忘门**负责决定保留多少上一时刻的单元状态到当前时刻的单元状态，即决定从细胞状态中丢弃什么信息。该门读取![{h_{t - 1}}](https://latex.csdn.net/eq?%7Bh_%7Bt%20-%201%7D%7D)和![{x_t}](https://latex.csdn.net/eq?%7Bx_t%7D)，然后经过sigmoid层后，输出一个0-1之间的数![{f_t}](https://latex.csdn.net/eq?%7Bf_t%7D)给每个在细胞状态![{C_{t - 1}}](https://latex.csdn.net/eq?%7BC_%7Bt%20-%201%7D%7D)中的数字逐点相乘。![{f_t}](https://latex.csdn.net/eq?%7Bf_t%7D)的值为0表示完全丢弃，1表示完全保留。

![img](https://i-blog.csdnimg.cn/blog_migrate/3ede78ba0a5b8f8f378db46a0b29e98c.gif)

**输入门**负责决定保留多少当前时刻的输入到当前时刻的单元状态，包含两个部分，第一部分为sigmoid层，该层决定要更新什么值，第二部分为tanh层，该层把需要更新的信息更新到细胞状态里。tanh层创建一个新的细胞状态值向量![{\tilde C_t}](https://latex.csdn.net/eq?%7B%5Ctilde%20C_t%7D)，![{\tilde C_t}](https://latex.csdn.net/eq?%7B%5Ctilde%20C_t%7D)会被加入到状态中。

![img](https://i-blog.csdnimg.cn/blog_migrate/8779a9f345fbfe34a4c452c621fc339b.gif)

然后就到了更新旧细胞状态的时间了，将![{C_{t - 1}}](https://latex.csdn.net/eq?%7BC_%7Bt%20-%201%7D%7D)更新为![{C_t}](https://latex.csdn.net/eq?%7BC_t%7D)，把旧状态与![{f_t}](https://latex.csdn.net/eq?%7Bf_t%7D)相乘，丢弃确定需要丢弃的信息，再加上![{i_t}*{\tilde C_t}](https://latex.csdn.net/eq?%7Bi_t%7D*%7B%5Ctilde%20C_t%7D) ，这样就完成了细胞状态的更新。

![img](https://i-blog.csdnimg.cn/blog_migrate/4f3e97ef1b375ef4c1c7c29bcb667011.gif)

**输出门**负责决定当前时刻的单元状态有多少输出，通过一个sigmoid层来确定细胞状态的哪个部分将输出出去。把细胞状态通过tanh进行处理，得到一个-1到1之间的值，并将它和sigmoid门的输出相乘，最终仅仅输出确定输出的部分。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9682d5ce2075e2450ef7125a0d2b43c9.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/223e377590625af199b2733219905bc8.png)

## 门控循环单元（GRU）

GRU 合并了 LSTM 的某些组件：

| 组件   | 功能                 |
| :----- | :------------------- |
| 更新门 | 决定保留多少旧信息   |
| 重置门 | 决定如何组合新旧信息 |

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f32178bf1c514cbdb6bdc6fffb940c73.png#pic_center)

重置门：

决定当前隐藏状态与之前隐藏状态的相关程度。它通过一个 Sigmoid 函数输出一个范围在 [0, 1] 之间的值，表示当前时间步要忘记多少之前的信息。

更新门：

控制当前时间步的隐藏状态更新的程度。它的输出也是一个 `[0, 1]` 之间的值，决定当前时刻的信息有多少来自于之前的状态。

## 注意力机制

注意力机制的核心思想是：**根据输入的不同部分对当前任务的重要性，动态分配不同的权重**。这种权重分配不是固定的，而是根据上下文动态计算的。

## Transformer 架构

Transformer 架构是一种基于自注意力机制（Self-Attention）的深度学习模型，由 Google 团队在 2017 年的论文[《Attention Is All You Need》](https://arxiv.org/abs/1706.03762)中首次提出。

![img](https://www.runoob.com/wp-content/uploads/2025/06/Transformer_full_architecture.png)

#### 1. 输入处理（底部）

- **Embeddings/Projections（嵌入/投影层）**
  - 作用：将输入的单词（或 token）转换成数字向量（比如 "猫" → [0.2, -0.5, 0.7…]）。
  - 类比：就像给每个单词分配一个独特的"身份证号码"，但更智能（包含语义信息）。

#### 2. 编码器（左侧）

- **Multi-Headed Self-Attention（多头自注意力）**
  - 作用：让模型同时关注输入中的所有单词，并计算它们之间的关系。
  - 举例：在句子"猫追老鼠"中，模型会学习"猫"和"老鼠"的关联比"猫"和"追"更强。
  - 关键：**并行处理所有单词**，不像RNN需要逐个计算。
- **Norm（层归一化）**
  - 作用：稳定训练过程，防止数值过大或过小（类似"调音量"到合适范围）。
- **Feed-Forward Network（前馈神经网络）**
  - 作用：对每个单词的表示进行进一步加工（比如提取更复杂的特征）。
  - 类比：像对"猫"的向量做一次深度解读，补充细节（比如"猫是哺乳动物"）。

#### 3. 解码器（右侧）

- **Masked Multi-Headed Self-Attention（掩码多头自注意力）**
  - 作用：训练时防止模型"作弊"（只能看到当前和之前的单词，不能看未来的）。
  - 举例：生成"我爱__"时，模型只能基于"我""爱"预测下一个词，不能提前知道答案是"你"。
- **Multi-Headed Cross-Attention（多头交叉注意力）**
  - 作用：让解码器询问编码器："关于输入，我应该重点关注什么？"
  - 场景：翻译任务中，解码器生成英文时，会参考编码器处理的中文输入。
- **Norm 和 Feed-Forward Network**
  - 与编码器类似，对解码器的表示进行归一化和深度处理。

#### 4. 输出（顶部）

- **Linear（线性层）**
  - 作用：将解码器的输出映射到词表（比如预测下一个词是"你"的概率最高）。
  - 举例：输入"我爱"，模型输出"你"的概率可能是80%，"吃饭"的概率是10%…

### 位置编码(Positional Encoding)

![img](https://www.runoob.com/wp-content/uploads/2025/06/dddd45f4sa4f87.png)

**参数说明：**

- `pos`：词在序列中的位置（如第 1 个词、第 2 个词等）。
- `i`：位置编码向量的维度索引（`0 ≤ i < d_model/2`）。
- `d_model`：位置编码的维度（通常与词向量的维度相同，如 512、768 等）。

## 序列到序列模型

Seq2Seq模型属于**编码器-解码器(Encoder-Decoder)**架构：

- **编码器**：将输入序列编码为一个固定长度的上下文向量(context vector)
- **解码器**：根据上下文向量逐步生成输出序列

![img](https://www.runoob.com/wp-content/uploads/2025/06/Seq2Seq.png)

### 基础架构组成

#### 编码器(Encoder)

编码器通常使用RNN(如LSTM或GRU)处理输入序列，逐步将序列信息压缩到隐藏状态中，最终生成代表整个输入序列的上下文向量。

#### 解码器(Decoder)

解码器从上下文向量开始，逐步生成输出序列的每个元素，直到产生结束标记。

### 工作流程

1. 编码器读取输入序列，生成上下文向量
2. 解码器初始化隐藏状态为上下文向量
3. 解码器逐步生成输出序列元素
4. 当生成结束标记时停止

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/Python-learning/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-08-01%20135912.png)

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/Python-learning/20260801150221431.png)

