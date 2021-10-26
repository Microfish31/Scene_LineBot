import re

# 是說縣市天氣嗎
def Weather(txt) :
    regex = re.compile(r'(市天氣|縣天氣)')
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

# 是說hello嗎
def Hello(txt) :
    regex = re.compile(r'(嗨)|(你好)|(您好)|(Hi)|(hi)|(Hello)|(hello)')
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

fun_list = [
            Weather,
            Hello
           ]

def ExistOrNot(get_text):
    for i in range(len(fun_list)) :
        if fun_list[i](get_text) :
           return i
    return -1
