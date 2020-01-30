from django.conf import settings
from pokemongogo.models import CounterInfo

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def counter_info(event, url):
    try:
        message = [
            ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))

def counter_template(event):
    try:
        message = TemplateSendMessage(
            alt_text='請選擇想要查的團體戰頭目',
            template=ButtonsTemplate(
                text='請選擇想要查的團體戰頭目',
                title='團體戰打手查詢',
                actions=[
                    MessageTemplateAction(
                        label='席多藍恩',
                        text='席多藍恩'
                    ),
                    MessageTemplateAction(
                        label='拉帝亞斯',
                        text='拉帝亞斯'
                    ),
                    MessageTemplateAction(
                        label='拉帝歐斯',
                        text='拉帝歐斯'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))

def not_found(event):
    try:
        message = TextSendMessage(
            text='抱歉! 查無資料'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))

def new_info(event):
    try:
        message = [
            TextSendMessage(
                text='鼠年行大運：和泡沫栗鼠還有紅色寶可夢一起慶祝農曆新年吧！'
            ),
            TextSendMessage(
                text='活動時間：2020年1月25日（星期六）清晨～2020年2月3日（星期一）'
            ),
            TextSendMessage(
                text='https://pokemongolive.com/zh_hant/post/lunar-2020/'
            )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))


def counter_target(target):
    try:
        unit = CounterInfo.objects.get(cName=target)
        return unit
    except:
        return None