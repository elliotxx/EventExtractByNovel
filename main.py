#coding=utf8
import os
import jieba
import jieba.posseg as pseg

filename = 'test.txt'

# 设置主题词
theme = [
'林雷',
]
theme = [w.decode('utf8') for w in theme]

# 设置事件类别
event_type = {
0:'修炼',
1:'说话',
2:'突破',
3:'战斗',
4:'行动',
}

# 自定义字典
jieba.add_word('林雷', 15, 'n')

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
	isTrigger = False
	for i, w in enumerate(words):
		if  w in theme and \
			( (i+1 < len(words) and flags[i+1]=='v') or\
			  (i+2 < len(words) and flags[i+2]=='v') ):
			# 这句话包含主题词 且 主题词后面两个词其中之一为动词
			if not isTrigger:
				print line
				isTrigger = True
			if i-1 >= 0:
				print words[i-1], flags[i-1]
			print w, flags[i]
			if i+1 < len(words):
				print words[i+1], flags[i+1]
			if i+2 < len(words):
				print words[i+2], flags[i+2]
			# break

	# 事件元素识别
	

	if isTrigger:
		os.system('pause')
