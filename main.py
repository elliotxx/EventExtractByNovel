#coding=utf8
import os
import jieba
import jieba.posseg as pseg

filename = 'test.txt'

trigger = [
'杀',
'突破',
'吃',
'说道',
'笑道',
'吼道',
'锻炼',
'扫',
'为首',
'瞧不起',
'修炼',
'闭关',
'打熬',
'锻炼',
'训练',
'扫向',
'诱导',
'羡慕',
'抓',
'甩',
'震',
'砸',
'拼命',
'名叫',		# v, 姓名，身份
]
trigger = [w.decode('utf8') for w in trigger]

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

	print words
	print flags

	# 匹配触发词
	for w, f in zip(words, flags):
		if 'v' in f and w in trigger:
			print line
			print w, f
			break

	# 事件元素识别
	


	os.system('pause')
