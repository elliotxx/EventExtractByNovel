#coding=utf8
import os
import jieba
import jieba.posseg as pseg
from sklearn import svm
from sklearn.model_selection import train_test_split
import numpy as np
from common import *

# 读取
path = 'data.txt'  # 数据文件路径
data = np.loadtxt(path, dtype=float, delimiter=',')	#, converters={4: iris_type})
# print data

# 分割为训练集和测试集
x, y = np.split(data, (16,), axis=1)
# x = x[:, :2]
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
# print x_train
# print y_train

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




filename = '《盘龙》.txt'.decode('utf8').encode('gb2312')
data_filename = 'data.txt'		# 字符串存储特征向量
# data_filename2 = 'data2.txt'	# unicode对应整型存储特征向量

# 设置主题词
theme = [
'林雷',
]
theme = [w.decode('utf8') for w in theme]

# 设置事件类别
event_type = {
1:'修炼',
2:'对话',
3:'心理活动',
}
event_type = {k:v.decode('utf8') for k,v in event_type.items()}

# 自定义字典
# jieba.add_word('林雷', 15, 'n')
# jieba.add_word('心中', 100, 'v')
# for feature_tag in feature_tag_list:
# 	jieba.add_word(feature_tag, 1)

# 打开小说文本（数据源）
fp = open(filename, 'rb')
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
	# isTrigger = False
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
			print 'Word freq:'
			print feature
			print 'Predict res:'
			y_hat = clf.predict(feature)
			predict_event_type = event_type[int(y_hat[0])]
			print predict_event_type
			print proba_list

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

			# os.system('pause')
			# print ''
			# break




	# 事件元素识别
	

	# if isTrigger:
	
fp.close()