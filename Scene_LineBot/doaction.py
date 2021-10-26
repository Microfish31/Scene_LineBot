from imgurpython import ImgurClient
from datetime import datetime
import parameter
import os
import requests
import json

Teamplates_Dirname = "Teamplates"

#type "message","json"
#obj type data
#access_token Line Notify access token
def LineNotifySend(type,obj,access_token) :
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
 
    params = {type: obj}
 
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    #print(r.status_code)

def UploadToImgur(client_data,name,title,description,album_id,file_path):
    description_data = description + "-" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    config = {
        'album': album_id,
        'name': name,
        'title': title,
        #'description': f'description-{datetime.now()} '
        'description': description_data
    }

    image = client_data.upload_from_path(file_path, config=config, anon=False)
    return image

def SendToImgur(album_id,name,title,description,file_path) :
    client = ImgurClient(parameter.client_id, parameter.client_secret, parameter.access_token, parameter.refresh_token)
    image = UploadToImgur(client,name,title,description,album_id,file_path)
    return  f"{image['link']}"

def WeatherDownload() :
    auth_key = parameter.cwb_auth_key
    Cwb_Dirname = "Cwb_Data"
    filepath = Cwb_Dirname + '//' + 'cwb_weather.json'

    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=" + auth_key + "&downloadType=WEB&format=JSON"
    response = requests.get(url)

    if os.path.isfile(filepath):
      print("檔案存在。")
    else:
      print("檔案不存在。")
      os.mkdir(Cwb_Dirname)

    with open(filepath,'wb') as f:
        f.write(response.content)

def FindFlexMsg(file_name) :
    FlexMessage = json.load(open(Teamplates_Dirname + "//" + file_name + ".json",'r',encoding='utf-8'))
    return FlexMessage

def FindRichMenusId(headers) :
    file_name = "richmenus_teamplate"
    rich_menu_data = json.dumps(FindFlexMsg(file_name)).encode('utf-8')
    dictt = json.loads(requests.request('POST', 'https://api.line.me/v2/bot/richmenu',headers=headers,data=rich_menu_data).text)
    return dictt['richMenuId']

def EnableRichMenu(Id,headers) :
    req = requests.request('POST', "https://api.line.me/v2/bot/user/all/richmenu/" + Id,headers=headers)
    return req.text