#coding=utf8
import os
import jieba
import jieba.posseg as pseg
import jieba.analyse
from common import *


# 自定义字典
jieba.add_word('林雷', 15, 'n')

# 若特征数据集文件不存在，那么创建一个
if not os.path.exists(train_data_filename):
	fp = open(train_data_filename,'w')
	fp.close()


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
			# 这句话包含主题词 且 主题词后面两个词其中之一为动词
			# 这个主题词没触发过
			if isTrigger[w]:
				continue
			# 触发成功
			# 构造特征向量
			feature = [line.count(feature_tag) for feature_tag in feature_tag_list]
			if not any(feature[:-1]):
				continue

			# 输出这句话
			isTrigger[w] = True
			print line

			# 输出关键词
			print 'Top 10 key:'
			tags = jieba.analyse.extract_tags(line, topK=10)
			print ','.join(tags)
			
			print 'Feature:'
			print feature

			# 构造特征数据集
			# 构造特征向量，存入本地
			label = raw_input()
			if label != '' and int(label) in range(1,len(event_type)+1):
				# 是预定事件类别
				label = int(label)
				feature.append(label)
				print 'Feature && label:'
				print feature
				print ''
				ft = open(train_data_filename, 'a')
				ft.write('%s\n'%(','.join([str(x) for x in feature])))
				ft.close()

fp.close()