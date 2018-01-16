## 【NLP】基于SVM的网络小说事件类型识别

## 依赖
* sklearn==0.19.1
* numpy==1.14.0
* scipy==1.0.0

## 文件目录
```
common.py - 放置公共变量和类
generate_feature.py - 手动特征向量，保存在本地
train_model.py - 使用SVM训练保存的特征向量，生成分类器
```

## 思路
1. 首先读取每句话，找到包含主题词的句子（主题词必须作为名词并且后两个词至少一个为动词），
2. 计算该句子的词频作为特征向量，如果全为0，则抛弃
3. 手动标注该特征向量的标签，即该句子属于哪个事件类别
4. 将所有标注过的特征向量和标签保存在本地
5. 使用SVM训练保存的特征向量，生成分类器
6. 继续读取每句话，找到包含主题词的句子，对该句子用分类器预测
7. 输出预测结果

## 事件类别
```
1 修炼
2 对话
3 心理活动
```

## 特征向量 Tag
```
腰部
发酸
麻麻
眯起
酸痛
歇息
打熬

咧嘴
说道
笑道
询问

感到
高兴
心中
忐忑
心底
坚定
```


## 参考资料
* Python中文分词组件 jieba  
http://www.oschina.net/p/jieba

* ICTCLAS 汉语词性标注集  
http://fhqllt.iteye.com/blog/947917

* Python中的支持向量机SVM的使用（有实例）  
https://www.cnblogs.com/luyaoblog/p/6775342.html

* 【Python】在Python中自定义迭代器Iterator  
http://blog.csdn.net/ghostfromheaven/article/details/11880251

* 文本分类与SVM  
http://blog.csdn.net/zhzhl202/article/details/8197109