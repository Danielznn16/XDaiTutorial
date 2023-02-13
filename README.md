# 第二次技术培训

大家好，之前振方已经分享过Docker的部署应用。考虑到大家都具有一定的Conda环境管理的经验，我们第二次技术培训主要聚焦于如何快速的把已有的工作做成demo方便汇报（本次不会介绍工业级的前端），基于此目前我们计划花半个小时至一个小时的时间给大家简单的介绍下。

**目录**

- [快速前端Streamlit](#----streamlit)
  * [基本的输入输出](#-------)
  * [一个简单的Demo](#-----demo)
- [后端快速搭建](#------)
  * [简单Json格式介绍](#--json----)
  * [Flask快速Get/Post请求封装](#flask--get-post----)
    + [Flask Get请求的例子](#flask-get-----)
    + [Flask Post请求的例子](#flask-post-----)
  * [FastAPI的模块化管理](#fastapi------)
  * [FastAPI的模块化管理](#fastapi-------1)
- [日志与数据管理（Mongo，pymongo；日常数据管理还有ES与Redis，不过我们不再进行展开了，需要时再学即可）](#--------mongo-pymongo---------es-redis---------------------)
  * [读、写的基本调用](#--------)
  * [数据更新与Upsert](#-----upsert)
  * [索引简介（方便起见，直接使用Compass、可以使用其他工具）](#--------------compass----------)
- [Git的使用](#git---)
  * [GitLab项目与群组的创建和人员增减（以公司的为例）](#gitlab---------------------)
  * [Access Token的创建与Git Clone](#access-token----git-clone)
  * [Git add commit push pull的基本使用](#git-add-commit-push-pull-----)
  * [Git branch 和 checkout、merge（简单的分支管理）](#git-branch---checkout-merge---------)
  * [Issue的创建与commit时如何引用](#issue----commit-----)
  * [Submodule简单介绍，与submodule-for的简单示例](#submodule------submodule-for-----)
  * [自动部署的简单介绍（日常科研不一定用得到，简单介绍下概念）](#-----------------------------)
- [Nginx简介（方便部署正式的工业级前端，与请求转发；Nginx只做简单介绍方便大家了解一个正式的前后端分离工程的部署）](#nginx----------------------nginx----------------------------)
  * [什么是Nginx](#---nginx)
  * [简单的负载均衡](#-------)
  * [请求转发](#----)
- [Bert 经典分类器训练](#bert--------)

## 快速前端Streamlit

Streamlit是一个快速前端，其特点是可以在Python端直接调用函数来在前端构造`Widget`(可以理解为前端的一个Object)和构造Widget并返回。其最方便的地方在于，其交互过程可以近似的视为一个流的过程因此当靠前的输入改变时，后面的输出会跟着改变（这一点很类似于以`React`为代表的一系列兼具效率与代码简洁性的前端方案）。其耦合了前后端，降低了初学者开发的难度（当然这也代表着牺牲了一定的定制化）。同时其仍然具有缓存机制，因此在调用一个本地模型的时候，可以不必每一次inference都重复加载模型。这些使得Streamlit非常适合机器学习工作者用来快速搭建Demo。

### 基本的输入输出

一个基本的Streamlit输入输出可以参考如下的形式

```python
# streamlit_io.py
# 引入Streamlit包
import streamlit as st

# 获取输入文本
text = st.text_input("Input Something")
# 输出文本
st.text(text)
```
之后运行

```bash
streamlit run streamlit_io.py
```

即可看到前端

![image-20230213144726349](https://github.com/Danielznn16/XDaiTutorial/blob/master/README.assets/image-20230213144457353.png)

### 一个简单的Demo

```python
# streamlit_demo.py
import streamlit as st

# mask_filling_llm 是我实现的一个输入Prompt返回分数和生成文本的函数
from api.LLM import mask_filling_llm
# markdown方法会把输入的文本当做Markdown进行渲染并展示到前端上
st.markdown("# Prompt Console")
st.markdown("## Input Panel")
# 使用text_area进行多行输入
input = st.text_area("Prompt")
# 判断是否空文本
if input:
  # 调用方法
	generated = mask_filling_llm(input)
	st.markdown("## Output")
  # 展示调用方法返回的信息
	st.markdown(f"### Score:\n{generated['logit'][0]}")
	st.markdown(f"### Generated:")
	st.text(generated['output'][0])
```

将这个前端启动，并实现`mask_filling_llm`即可得到

![image-20230213144726349.png](https://github.com/Danielznn16/XDaiTutorial/blob/master/README.assets/image-20230213144726349.png)

## 后端快速搭建

后端快速搭建涵盖了以下几个方面：简单Json格式介绍、Flask快速Get/Post请求封装以及FastAPI的模块化管理。

### 简单Json格式介绍

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式，它的语法与JavaScript对象表示法相似。Json格式有如下特点：

1. Json使用了JavaScript语法中的对象和数组。
2. Json是一个字符串，用于传输或存储数据。
3. Json的数据结构非常简洁，易于阅读和编写。

Json具有轻量级、易于读写等优点，被广泛应用在web开发中。Json数据以键值对的形式存储，数据类型包括数字、字符串、布尔值、数组、对象等。

下面是一个Json格式的例子：

```json
{
    "name": "John Doe",
    "age": 35,
    "address": {
        "street": "1234 Main St",
        "city": "San Francisco",
        "state": "CA"
    },
    "phoneNumbers": [
        {
            "type": "home",
            "number": "555-555-1234"
        },
        {
            "type": "work",
            "number": "555-555-4321"
        }
    ]
}
```

### Flask快速Get/Post请求封装

Flask是一个简单的Python Web框架，它支持快速的Get/Post请求封装。

#### Flask Get请求的例子

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name')
    return 'Hello, {}!'.format(name)

if __name__ == '__main__':
    app.run()
```

#### Flask Post请求的例子

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/data', methods=['POST']) # methods可以用来指定允许的请求类型
def handle_data():
    data = request.get_json()
    # Do something with the data
    return data

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI的模块化管理

FastAPI允许我们把多个API路由分别存放在不同的模块，以方便代码维护。我们可以在主文件中通过加载模块并注册路由实现这一功能。

例如，我们可以把所有位于`/user/*`路由下的服务封装进一个名为`user.py`的文件中，它的内容如下：

```python
# user.py
from fastapi import FastAPI
app = FastAPI()

@app.post("/user/signup")
def signup_user(username: str, password: str):
    return {"username": username, "password": password}

@app.get("/user/{user_id}")
def get_user_by_id(user_id: int):
    return {"user_id": user_id}
```

然后，在主文件中加载该模块并注册路由：

```python
from fastapi import FastAPI
from .user import app as user_app

app = FastAPI()

app.include_router(user_app, prefix="/user")
```

同样的，我们可以为对话服务创建一个名为`conversation.py`的文件：

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/conversation")
def start_conversation(text: str):
    return {"text": text}

@app.get("/conversation/{conversation_id}")
def get_conversation_by_id(conversation_id: int):
    return {"conversation_id": conversation_id}
```

好的，那么更新后的内容如下：

### FastAPI的模块化管理

FastAPI允许我们把多个API路由分别存放在不同的模块，以方便代码维护。我们可以在主文件中通过加载模块并注册路由实现这一功能。

例如，我们可以把所有位于`/user/*`路由下的服务封装进一个名为`user.py`的文件中，它的内容如下：

```python
pythonCopy code
from fastapi import FastAPI

app = FastAPI()

@app.post("/signup")
def signup_user(username: str, password: str):
    return {"username": username, "password": password}

@app.get("/{user_id}")
def get_user_by_id(user_id: int):
    return {"user_id": user_id}
```

然后，在主文件中加载该模块并注册路由：

```python
pythonCopy code
from fastapi import FastAPI
from .user import app as user_app

app = FastAPI()

app.include_router(user_app, prefix="/user") # 这样/user/signup调用的就是signup_user
```

同样的，我们可以为对话服务创建一个名为`conversation.py`的文件：

```python
pythonCopy code
from fastapi import FastAPI

app = FastAPI()

@app.post("/")
def start_conversation(text: str):
    return {"text": text}

@app.get("/{conversation_id}")
def get_conversation_by_id(conversation_id: int):
    return {"conversation_id": conversation_id}
```

最后，在主文件中加载该模块并注册路由：

```python
from fastapi import FastAPI
from .user import app as user_app
from .conversation import app as conversation_app

app = FastAPI()

app.include_router(user_app, prefix="/user")
app.include_router(conversation_app, prefix="/conversation")
```

这种方法的好处是，即使应用的路由很多，只要路由在同一个模块下，可以非常容易地管理，也可以方便地将同一类型的路由模块抽象出来，达到复用的目的。

## 日志与数据管理（Mongo，pymongo；日常数据管理还有ES与Redis，不过我们不再进行展开了，需要时再学即可）

MongoDB是一种文档型数据库，与传统的关系型数据库不同，MongoDB以文档的形式存储数据，每个文档代表一个数据记录，并通过键值对的方式来组织数据。pymongo是一个与MongoDB交互的python库，可以用来读写数据。

日常数据管理中，除了MongoDB还有其他数据库如ES与Redis，它们分别用于处理全文检索与缓存，但是由于这些不是我们本文的重点，所以不再详细展开。

### 读、写的基本调用

如果要使用MongoDB进行数据管理，需要先安装MongoDB和pymongo。可以使用以下命令安装：

```bash
pip install pymongo
```

使用pymongo连接到MongoDB，代码如下：

```python
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database_name"]
collection = db["collection_name"]
```

读数据可以通过find方法来实现，返回结果是一个游标，可以迭代访问所有数据：

```python
# 查询所有记录
cursor = collection.find({})
for record in cursor:
    print(record)
```

写入数据，代码如下：

```python
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

posts = db.posts
post_id = posts.insert_one(post).inserted_id
```

读取数据，代码如下：

```python
query = {"author": "Mike"}
new_values = {"$set": {"text": "My updated blog post!"}}

posts.update_one(query, new_values)
```

### 数据更新与Upsert

更新数据，代码如下：

```python
query = {"author": "Mike"}
new_values = {"$set": {"text": "My updated blog post!"}}

posts.update_one(query, new_values)
```

Upsert，代码如下：

```python
query = {"author": "non_existing_author"}
new_values = {"$set": {"text": "My updated blog post!"}}

posts.update_one(query, new_values, upsert=True)
```

### 索引简介（方便起见，直接使用Compass、可以使用其他工具）

索引是对数据库中的数据进行组织的一种方式，有助于提高查询效率。

可以直接在Compass，选择Colllection的index，构造索引。

## Git的使用

### GitLab项目与群组的创建和人员增减（以公司的为例）

### Access Token的创建与Git Clone

### Git add commit push pull的基本使用

### Git branch 和 checkout、merge（简单的分支管理）

### Issue的创建与commit时如何引用
### Submodule简单介绍，与submodule-for的简单示例
### 自动部署的简单介绍（日常科研不一定用得到，简单介绍下概念）

## Nginx简介（方便部署正式的工业级前端，与请求转发；Nginx只做简单介绍方便大家了解一个正式的前后端分离工程的部署）

### 什么是Nginx

### 简单的负载均衡

### 请求转发

## Bert 经典分类器训练

Note: 除了Demo之外，虽然现在超大模型的影响力与日俱增，但BERT等模型的使用还是很多的。因此我还会顺带过一下经典的Bert分类器训练（使用transformers库的trainer）