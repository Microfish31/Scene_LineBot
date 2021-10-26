from linebot.models import MessageEvent, TextMessage, TextSendMessage,StickerMessage,LocationMessage,StickerSendMessage,ImageMessage,ImageSendMessage,LocationSendMessage,ImagemapSendMessage,TemplateSendMessage,URIImagemapAction,BaseSize,ImagemapArea,ButtonsTemplate,DatetimePickerTemplateAction,MessageTemplateAction,URITemplateAction,ConfirmTemplate,PostbackTemplateAction,CarouselColumn,CarouselTemplate,ImageCarouselTemplate,ImageCarouselColumn,MessageAction,QuickReply,QuickReplyButton,FlexSendMessage,PostbackEvent
import configparser
from linebot import LineBotApi, WebhookHandler
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
import json
import doaction

App = Flask(__name__)
config = configparser.ConfigParser()

Photo_Dir_Name = "Photos"
Setting_Dir_Name = "Setting"

@App.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    App.logger.info("Request body: " + body)
    
    #print(signature)
    try:
        #print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# LINE 聊天機器人的基本資料設置
def LineBotSet() :
    global line_bot_api
    global handler
    config.read('config.ini')

    # Set
    author_key =  config.get('line-bot', 'channel_access_token')
    line_bot_api = LineBotApi(author_key)
    handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

    settings_path = Setting_Dir_Name + "//" + "settings.json"

    with open(settings_path,'r') as f:
        setting_dict =  json.load(f)

    if setting_dict["RichMenuFlag"] == '0' :
        #..................................
        # Rich Menu
        headers = {"Authorization":"Bearer " + author_key,"Content-Type":"application/json"}

        Id = doaction.FindRichMenusId(headers)

        with open(Photo_Dir_Name + "//" + "default_rich_menu.png",'rb') as f:
            line_bot_api.set_rich_menu_image(Id, "image/png", f)

        print(doaction.EnableRichMenu(Id,headers))

        setting_dict["RichMenuFlag"] = "1"

        with open(settings_path,'w') as f:
            json.dump(setting_dict,f)
        #...................................
