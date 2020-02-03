from django.conf import settings
from pokemongogo.models import CounterInfo
from pokemongogo.models import News
from pokemongogo.models import PttArticles

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

import requests
from bs4 import BeautifulSoup

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

def get_news():
    """
    爬蟲部分
    1. 取得寶可夢官方網站最新貼文
    2. 用 try 檢查資料庫是否已存在同筆資料
    3. 回傳 3 個變數給 news_info(): 文章標題、時間、連結
    """
    base_url = 'https://pokemongolive.com'
    post_url = base_url + '/zh_hant/post'
    
    resp = requests.get(post_url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html5lib')
    
    time = soup.select('.post-list__date')[0].text.strip()
    title = soup.select('a')[5].text.strip()
    url = soup.select('a')[5].get('href')
    news_url = base_url + url
    
    try:
        # 資料已存在 -> 有抓到同title的entry
        unit = News.objects.get(cName=title)
    except:
        # 有新資訊 -> 新增進資料庫
        unit = News.objects.create(cName=title, cDate=time, cUrl=news_url)
        unit.save()

    return title, time, news_url

def new_info(event):
    title, time, news_url = get_news()       
    try:
        message = [
            TextSendMessage(
                text='【'+time+'】\n'+title
            ),
            TextSendMessage(
                text=news_url
            )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))


def get_ptt():
    ptt_url = 'https://www.ptt.cc'
    pokemon_url = '/bbs/PokemonGO/index.html'
    
    def get_page(url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text
        else:
            return None

    def get_article(dom):
        soup = BeautifulSoup(dom, 'html5lib')
        previous_url = soup.select('div a')[7].get('href')
        data = soup.find_all('div', 'r-ent')
        
        articles = []        
        for d in data:     
            push_count = 0
            push = d.find('div', 'nrec').text.strip()
            if push:
                try:
                    push_count = int(push)
                except:
                    if push == '爆':
                        push_count = 99
                    elif push.startswith('X'):
                        push_count = -10
        
            if d.find('a'):
                title = d.find('div', 'title').text.strip()
                time = d.find('div', 'date').text.strip()
                url = ptt_url + d.find('a')['href']
                if push_count > 50 and '公告' not in title:
                    articles.append({
                        'push': push_count,
                        'title': title,
                        'date': time,
                        'url': url
                    })
    
        return articles, previous_url

    articles = []
    counter = 0
    current_page = get_page(ptt_url+pokemon_url)
    while counter < 2:
        data, previous_url = get_article(current_page)
        articles += data
        current_page = get_page(ptt_url+previous_url)
        counter += 1
    
    return articles
    
def ptt_info(event):
    articles = get_ptt()
    for article in articles:
        cName = article['title']
        cDate = article['date']
        cUrl = article['url']
        try:
            unit = PttArticles.objects.get(cName=cName)
        except:
            unit = PttArticles.objects.create(cName=cName, cDate=cDate, cUrl=cUrl)
            unit.save() 
    try:
        text = ''
        for i in reversed(range(1,10)):
            try:
                unit = PttArticles.objects.get(id=i)
                text += unit.cName
                text += '\n'
                text += unit.cUrl
                text += '\n\n'
            except:
                pass
        message = [
            TextSendMessage(
                text=text
            ),
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