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
                    unit = func.counter_target(mtext)
                    if unit:
                        func.counter_info(event, unit.cUrl)
                    elif mtext == '團體戰打手':
                        func.counter_template(event)
                    elif mtext == '最新消息':
                        func.new_info(event)
                    elif mtext.lower() == 'ptt':
                        func.ptt_info(event)
                    else:
                        func.not_found(event)
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()