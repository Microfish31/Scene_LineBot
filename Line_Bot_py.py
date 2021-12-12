import Setting.parameter as parameter
import Module.regex as regex
import Module.line_tool as line_tool
import Module.data_analysis as data_analysis
# 底線暫時不用理會
import Module.doaction as doaction
import Module.scrapying as scrapying

from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
#...........................................................................................
App = Flask(__name__)
handler,line_bot_api = line_tool.LineBotSet()
#...........................................................................................

@App.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    App.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def RegexResult(work_num,get_str) :
    if work_num == 0 :
        location = (get_str.split('天氣'))[0]
        if parameter.city.get(location,False) :
           citynum = int(parameter.city[location])
           doaction.WeatherDownload()
           data_analysis.Weather30Hr(citynum)
           return line_tool.FlexSendMessage('[天氣]',doaction.FindFlexMsg('weather_teamplate'))
        else :
           return line_tool.TextSendMessage("查無此縣市")
    elif work_num == 1 :   
        txt = "你好呀!"
        return line_tool.TextSendMessage(txt)
    elif work_num == 2 :   
        return line_tool.FlexSendMessage('[使用選擇]',doaction.FindFlexMsg('destination_choice_template'))
    elif work_num == 3 :   
        data_analysis.RenewSiteTemplate()
        return line_tool.FlexSendMessage('[景點資訊]',doaction.FindFlexMsg('site_template'))
    elif work_num == 4 :
        data_analysis.RenewNearSiteTemplate()   
        return line_tool.FlexSendMessage('[附近景點資訊]',doaction.FindFlexMsg('site_near_template'))
    return None

# 回應 TextMessage
@handler.add(line_tool.MessageEvent, message=line_tool.TextMessage)
def TextEcho(event):
    if event.message.text == "說明":  
        reply_msg = line_tool.TextSendMessage("哈哈，暫時沒有說明。")
    elif event.message.text == "製作團隊" :
        reply_msg = line_tool.FlexSendMessage('[製作團隊]',doaction.FindFlexMsg('maker'))
    else :
        b = regex.ExistOrNot(event.message.text)
        if b != -1 :
           reply_msg = RegexResult(b,event.message.text)
        else :    
           reply_msg = line_tool.TextSendMessage("我聽不懂唷 @@")

    line_bot_api.reply_message(event.reply_token,reply_msg)


# 回應 StickerMessage
@handler.add(line_tool.MessageEvent, message = line_tool.StickerMessage)
def StickerEcho(event):
    line_bot_api.reply_message(event.reply_token,line_tool.StickerSendMessage(package_id=1, sticker_id=2))

# 回應 LocationMessage
@handler.add(line_tool.MessageEvent, message = line_tool.LocationMessage)
def LocationEcho(event):
    address_txt = str(event.message.address)
    latitude_txt = str(event.message.latitude)
    longitude_txt = str(event.message.longitude)
    title_txt = str(event.message.title)
    txt = "了解! 我解讀您的位置在:\n" + address_txt + "\n" + latitude_txt + "\n"+ longitude_txt + "\n" + title_txt
    line_bot_api.reply_message(event.reply_token,line_tool.TextSendMessage(txt))

# 回應 ImageMessage
@handler.add(line_tool.MessageEvent, message = line_tool.ImageMessage)
def ImageEcho(event):
    url_a = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/NCULogo.svg/1200px-NCULogo.svg.png'
    line_bot_api.reply_message(event.reply_token,line_tool.ImageSendMessage(original_content_url= url_a, preview_image_url= url_a))

if __name__ == "__main__":
    App.run()
