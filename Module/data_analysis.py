from math import cos
from math import sin
import math
import json
import random

Teamplates_Dirname = "Teamplates"

def Rad(d):
    return d * math.pi / 180.0

def GetDistance(lat1_txt, lng1_txt, lat2_txt, lng2_txt):
    lat1 = float(lat1_txt)
    lng1 = float(lng1_txt)
    lat2 = float(lat2_txt)
    lng2 = float(lng2_txt)
    EARTH_REDIUS = 6378.137
    radLat1 = Rad(lat1)
    radLat2 = Rad(lat2)
    a = radLat1 - radLat2
    b = Rad(lng1) - Rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(sin(a/2), 2) + cos(radLat1) * cos(radLat2) * math.pow(sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s

def Weather30Hr(citynum) :
    time = ['','','']
    rain_chance = ['','','']
    wx = ['','','']
    cci = ['','','']
    maxt = ['','','']
    mint = ['','','']

    data =  json.load(open('Cwb_Data//cwb_weather.json','r',encoding='utf-8'))

    location = data['cwbopendata']['dataset']['location'][citynum]['locationName']
    
    for j in range(3) :
        get = data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][0]['time'][j]['startTime'].split('T') 
        getdate = get[0]
        gethour = get[1].split('+') 
        time[j] = getdate + ' ' + gethour[0]
        rain_chance[j] = data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][4]['time'][j]['parameter']['parameterName']
        wx[j] =          data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][0]['time'][j]['parameter']['parameterName']
        cci[j] =          data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][3]['time'][j]['parameter']['parameterName']
        maxt[j] =        data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][1]['time'][j]['parameter']['parameterName']
        mint[j] =        data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][2]['time'][j]['parameter']['parameterName']
        RenewWeatherTeamplate(location,time,rain_chance,wx,cci,maxt,mint)

def RenewWeatherTeamplate(location,time,rain_chance,wx,cci,maxt,mint):
    path = Teamplates_Dirname + "//" + "weather_teamplate.json"
    data =  json.load(open(path,'r'))
    
    for i in range(3) :
        data['contents'][i]['header']['contents'][0]['contents'][0]['text'] = location
        data['contents'][i]['header']['contents'][1]['text'] = time[i]
        data['contents'][i]['header']['contents'][2]['contents'][1]['text']  = rain_chance[i]+"%"
        a = rain_chance[i]
        if a == "0": 
            a = "0.01"
        data['contents'][i]['header']['contents'][3]['contents'][0]['width'] = a + "%"
        data['contents'][i]['body']['contents'][0]['contents'][0]['text']  = wx[i]
        data['contents'][i]['body']['contents'][1]['contents'][0]['text']  = cci[i]
        data['contents'][i]['body']['contents'][2]['contents'][1]['text'] = maxt[i]+"°C"
        data['contents'][i]['body']['contents'][3]['contents'][1]['text'] = mint[i]+"°C"

    f = open(path,'w')
    json.dump(data,f)
    f.close()

def RenewSiteTemplate():
    path = Teamplates_Dirname + "//" + "site_template.json"
    data =  json.load(open(path,'r'))
    x=int(random.uniform(100,199))
    data['body']['contents'][0]['text'] = "九份  測試變數:"+str(x)
    data['body']['contents'][1]['text'] = "天氣:⛅晴天  測試變數:"+str(x)
    data['body']['contents'][2]['text'] = "濕度:38%  測試變數:"+str(x)
    data['body']['contents'][3]['text'] = "人流:75%  測試變數:"+str(x)
    
    f = open(path,'w')
    json.dump(data,f)
    f.close()

def RenewNearSiteTemplate():
    path = Teamplates_Dirname + "//" + "site_near_template.json"
    data =  json.load(open(path,'r'))
    x=int(random.uniform(100,199))
    for i in range(3):
        data['contents'][i]['body']['contents'][0]['text'] = "九份  測試變數:"+str(x)
        data['contents'][i]['body']['contents'][1]['text'] = "天氣:⛅晴天  測試變數:"+str(x)
        data['contents'][i]['body']['contents'][2]['text'] = "濕度:38%  測試變數:"+str(x)
        data['contents'][i]['body']['contents'][3]['text'] = "人流:75%  測試變數:"+str(x)
    f = open(path,'w')
    json.dump(data,f)
    f.close()
    