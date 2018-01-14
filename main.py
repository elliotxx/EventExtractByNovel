#coding=utf8
import os
import jieba
import jieba.posseg as pseg
import jieba.analyse
from common import *

# filename = 'test.txt'
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
jieba.add_word('林雷', 15, 'n')
# jieba.add_word('心中', 100, 'v')
# for feature_tag in feature_tag_list:
# 	jieba.add_word(feature_tag, 1)

# 若特征数据集文件不存在，那么创建一个
if not os.path.exists(data_filename):
	fp = open(data_filename,'w')
	fp.close()

# 若特征数据集文件不存在，那么创建一个
# if not os.path.exists(data_filename2):
# 	fp = open(data_filename2,'w')
# 	fp.close()

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
	for i, w in enumerate(words):
		if  w in theme and \
			( (i+1 < len(words) and flags[i+1]=='v') or\
			  (i+2 < len(words) and flags[i+2]=='v') ) and\
			(i-1 >= 0 and 'v' not in flags[i-1]):
			# 这句话包含主题词 且 主题词后面两个词其中之一为动词
			# 触发成功
			# 构造特征向量
			feature = [line.count(feature_tag) for feature_tag in feature_tag_list]
			if not any(feature[:-1]):
				continue

			# 输出这句话
			print line

			# 记录是否第一次触发
			# if not isTrigger:
			# 	print line
			# 	isTrigger = True

			# 输出相邻词性
			# if i-1 >= 0:
			# 	print words[i-1], flags[i-1]
			# print w, flags[i]
			# if i+1 < len(words):
			# 	print words[i+1], flags[i+1]
			# if i+2 < len(words):
			# 	print words[i+2], flags[i+2]

			# 输出关键词
			print 'Top 10 key:'
			tags = jieba.analyse.extract_tags(line, topK=10)
			print ','.join(tags)
			
			print 'Word freq:'
			print feature
			# seg_list = jieba.cut(line)
			# print ','.join(seg_list)
			
			# if len(tags)<10:
			# 	tags += ['']*(10-len(tags))
			# tags_str = ','.join(tags) 
			# print tags_str
			# tags_str2 = ','.join([ ''.join([str(ord(x)) for x in tag]) for tag in tags])
			# print tags_str2

			# 构造特征数据集
			# 构造特征向量，存入本地


			label = raw_input()
			if label != '' and int(label) in range(1,len(event_type)+1):
				# 是预定事件类别
				label = int(label)
				feature.append(label)
				print 'Feature:'
				print feature
				print ''
				ft = open(data_filename, 'a')
				# ft.write('%s,%s\n'%(tags_str.encode('utf8'), event_type[label].encode('utf8')))
				ft.write('%s\n'%(','.join([str(x) for x in feature])))
				ft.close()
				# ft = open(data_filename2, 'a')
				# # ft.write('%s,%s\n'%(tags_str2, event_type[label].encode('utf8')))
				# ft.write('%s,%s\n'%(tags_str2, str(label)))
				# ft.close()
			break

	# 事件元素识别
	

	# if isTrigger:
	# 	os.system('pause')
fp.close()