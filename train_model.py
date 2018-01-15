#coding=utf8
import os
import jieba
import jieba.posseg as pseg
from sklearn import svm
from sklearn.model_selection import train_test_split
import numpy as np
from common import *


# 训练分类器
# 读取
data = np.loadtxt(train_data_filename, dtype=float, delimiter=',')

# 分割为训练集和测试集
x, y = np.split(data, (16,), axis=1)
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)

# 训练svm分类器
# clf = svm.SVC(C=0.1, kernel='linear', decision_function_shape='ovr')
clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr', probability=True)
clf.fit(x_train, y_train.ravel())

# 计算svc分类器的准确率
print 'Train accuracy:'
print clf.score(x_train, y_train)  # 精度
y_hat = clf.predict(x_train)
# show_accuracy(y_hat, y_train, '训练集')
print 'Test accuracy:'
print clf.score(x_test, y_test)
# print x_test
y_hat = clf.predict(x_test)
print 'Predict ans:'
print y_hat
# show_accuracy(y_hat, y_test, '测试集')


# 使用分类器预测
# 打开小说文本（数据源）
fp = open(text_filename, 'rb')
for line in fp:
	# 提取每句话
	line = line.decode('utf8').strip()
	if len(line) == 0:
		continue

	# 对每句话进行词性标注
	res = pseg.cut(line)
	words = []
	flags = []
	for w in res:
		words.append(w.word)
		flags.append(w.flag)


	# 匹配触发词
	isTrigger = {k:False for k in theme}
	for i, w in enumerate(words):
		if  w in theme and \
			( (i+1 < len(words) and flags[i+1]=='v') or\
			  (i+2 < len(words) and flags[i+2]=='v') ) and\
			(i-1 >= 0 and 'v' not in flags[i-1]):
			# 这个主题词没触发过
			if isTrigger[w]:
				continue
			# 这句话包含主题词 且 主题词后面两个词其中之一为动词
			# 触发成功
			# 构造特征向量
			feature = [line.count(feature_tag) for feature_tag in feature_tag_list]
			if not any(feature[:-1]):
				continue
			feature = np.array([[float(x) for x in feature]])

			# 筛掉预测率低于80%的结果
			proba_list = clf.predict_proba(feature)
			if not (any([x>0.7 for x in proba_list[0]])):
				continue 

			# 输出预测信息
			isTrigger[w] = True
			print line
			print 'Feature:'
			print feature
			print 'Predict res:'
			y_hat = clf.predict(feature)
			predict_event_type = event_type[int(y_hat[0])]
			print predict_event_type
			print proba_list
			print ''

			# 将结果输出到对应的文件中
			filename_temp = '%s_%s.txt'%(w.encode('gbk'), predict_event_type.encode('gbk'))
			if not os.path.exists(filename_temp):
				ft = open(filename_temp, 'w')
				ft.close()
			ft = open(filename_temp, 'a')
			ft.write(line.encode('utf8'))
			ft.write('\n')
			ft.write('\n')
			ft.close()

			os.system('pause')
	
fp.close()