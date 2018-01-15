#coding=utf8
feature_tag_list = [
'腰部',
'发酸',
'锻炼',
'修炼',
'酸痛',
'歇息',
'打熬',

'说道',
'笑道',
'询问',

'感到',
'高兴',
'心中',
'忐忑',
'心底',
'坚定',
]

# 设置主题词
theme = [
'林雷',
]

# 设置事件类别
event_type = {
1:'修炼',
2:'对话',
3:'心理活动',
}

# 文件名
text_filename = '《盘龙》.txt'
train_data_filename = 'train_data.txt'		# 字符串存储特征向量和对应标签


# 预处理部分
# 全部转换为 unicode 存储
global feature_tag_list, theme, event_type, text_filename, train_data_filename
feature_tag_list = [x.decode('utf8') for x in feature_tag_list]
theme = [w.decode('utf8') for w in theme]
event_type = {k:v.decode('utf8') for k,v in event_type.items()}

# 文件名转换为 gbk 编码
text_filename = '《盘龙》.txt'.decode('utf8').encode('gbk')
