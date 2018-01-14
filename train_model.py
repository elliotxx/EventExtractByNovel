#coding=utf8
from sklearn import svm
from sklearn.model_selection import train_test_split
import numpy as np
# 读取
path = 'data2.txt'  # 数据文件路径
data = np.loadtxt(path, dtype=float, delimiter=',')	#, converters={4: iris_type})
# print data

# 分割为训练集和测试集
x, y = np.split(data, (10,), axis=1)
# x = x[:, :2]
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
print x_train, y_train

# 训练svm分类器
# clf = svm.SVC(C=0.1, kernel='linear', decision_function_shape='ovr')
clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
clf.fit(x_train, y_train.ravel())

# 计算svc分类器的准确率
print clf.score(x_train, y_train)  # 精度
y_hat = clf.predict(x_train)
show_accuracy(y_hat, y_train, '训练集')
print clf.score(x_test, y_test)
y_hat = clf.predict(x_test)
show_accuracy(y_hat, y_test, '测试集')