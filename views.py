from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import TextMessage, MessageEvent

from module import func
from pokemongogo.models import CounterInfo

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# Create your views here.
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    #unit_exist = func.data_exist(mtext)
                    #if unit_exist:
                    #    func.counter_info(event, mtext)
                    #elif mtext == '團體戰打手':
                    #    func.counter_template(event)
                    if mtext == '最新消息':
                        func.get_news(event)
                    elif mtext == 'PTT':
                        func.get_ptt(event)
                    elif mtext == '頭目一覽':
                        func.get_allBoss(event)
                    elif mtext == '使用說明':
                        func.intro(event)
                    elif mtext == '團體戰打手':
                        func.get_current_counter(event)
                    elif mtext[:2] == '湯姆':
                        try:
                            search_range = int(mtext[2:])
                        except:
                            search_range = 1
                        func.get_tomchun(event, search_range)
                    else:
                        func.other(event, mtext)
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
