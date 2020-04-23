from django.conf import settings
from pokemongogo.models import CounterInfo
from pokemongogo.models import News
from pokemongogo.models import PttArticles

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

import requests
from bs4 import BeautifulSoup
from datetime import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def get_page(url):
    """
    【爬蟲】基本程式
    * 回傳 soup 物件
    """
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html5lib')
    return soup

def get_allBoss(event):
    """
    【頭目一覽】
    1. 爬 LeekDuck 網站
    2. 抓圖片網址，特殊字元轉換 (空格 = %20，é = %C3%A9)
    3. 回覆圖片網址給使用者
    """
    base_url = 'https://leekduck.com'
    boss_url = '/boss/'
    soup = get_page(base_url+boss_url)
    allboss_imgurl = base_url + soup.find('p', id='graphic').img['src'].replace(' ', '%20')
    if 'é' in allboss_imgurl: #處理Pokémon特殊字元
        allboss_imgurl = allboss_imgurl.replace('é', '%C3%A9')
    try:
        message = ImageSendMessage(
            preview_image_url=allboss_imgurl,
            original_content_url=allboss_imgurl
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(e.__class__.__name__))

def get_current_counter(event):
    """
    【團體戰打手】
    1. 爬 LeekDuck 網站
    2. 取得常規團體戰和SP團體戰的頁面
    3. 利用 raid_bosses 函式回傳的 list 回傳活動剩餘時間和圖片網址給使用者
    4. 當有 3 個以上團體戰時，只顯示圖片 (因 Line 的限制只能 5 則訊息)
    """
    def convert_timedelta(duration):
        """
        【時間格式轉換】
        * 回傳 4 個變數: days, hours, minutes, seconds
        """
        days, seconds = duration.days, duration.seconds + 3600*8 # 與網站的時間同步
        hours = seconds // 3600
        if hours > 23:
            days += 1
            hours -= 24
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return days, hours, minutes, seconds
    
    def raid_bosses(boss_div):
        """
        【爬蟲】尋找頁面上所有團體戰
        1. 時間顯示若異常，所有時間的變數 = "??"
        2. 圖片網址特殊字元轉換 (空格 = %20)
        3. 若無圖片，找封面圖；若無封面圖，網址 = "找不到圖片"
        4. 最後回傳 2 個list: 活動剩餘時間 (boss_list), 圖片網址 (img_list)
        """
        boss_list = []
        img_list = []
        today = datetime.now()
        
        for boss in boss_div:
            text = boss.find('div', 'event-text')
            
            try: #時間顯示正常
                t = text.find('p')['data-event-list-date'].split('+')[0]
                t = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
                time_rest = t - today
                days, hours, minutes, seconds = convert_timedelta(time_rest)
            except: #時間異常
                days, hours, minutes, seconds = '??', '??', '??', '??'

            if days == '??' or days >= 0: #篩選出尚未結束的活動
                link = boss.parent['href']
                soup_img_page = get_page(base_url+link)
                
                if soup_img_page.find('p', id='graphic1'): #有攻略
                    try:
                        img_url = soup_img_page.find('p', id='graphic1').img['src'].replace(' ', '%20')
                    except:
                        img_url = '找不到圖片QQ'
                
                else: #無攻略，以封面圖片替代
                    try:
                        img_url = soup_img_page.find('div', 'event-cover-image').img['src']
                    except:
                        img_url = '找不到圖片QQ'
                    
                countdown = '活動倒數: {days}天{hours}小時{minutes}分'.format(**locals())
                boss_list.append(countdown)
                img_list.append(base_url + img_url)
            else:   
                pass
        
        return boss_list, img_list

    base_url = 'https://leekduck.com'
    event_url = '/events/'

    soup = get_page(base_url+event_url)
    content = soup.find('div', 'events-list current-events')
    bosses = content.find_all('div', 'event-item-wrapper raid-battles')
    bosses_sp = content.find_all('div', 'event-item-wrapper raid-weekend')
    
    boss_list, img_list = raid_bosses(bosses+bosses_sp)
    text_list = [i for i in boss_list]
    imgUrl_list =  [j for j in img_list]
    
    # 判斷要傳多少訊息給使用者，最多 1 個常態BOSS + 2 個周末sp BOSS
    if len(text_list) == 1:
        try:
            message = [
                TextSendMessage(
                    text=text_list[0]
                ),
                ImageSendMessage(
                    preview_image_url=imgUrl_list[0],
                    original_content_url=imgUrl_list[0]
                )
            ]
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(e.__class__.__name__))

    elif len(text_list) == 2:
        try:
            message = [
                TextSendMessage(
                    text=text_list[0]
                ),
                ImageSendMessage(
                    preview_image_url=imgUrl_list[0],
                    original_content_url=imgUrl_list[0]
                ),
                TextSendMessage(
                    text=text_list[1]
                ),
                ImageSendMessage(
                    preview_image_url=imgUrl_list[1],
                    original_content_url=imgUrl_list[1]
                )
            ]
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(e.__class__.__name__))

    elif len(text_list) == 3:
        try:
            message = [
                ImageSendMessage(
                    preview_image_url=imgUrl_list[0],
                    original_content_url=imgUrl_list[0]
                ),
                ImageSendMessage(
                    preview_image_url=imgUrl_list[1],
                    original_content_url=imgUrl_list[1]
                ),
                ImageSendMessage(
                    preview_image_url=imgUrl_list[2],
                    original_content_url=imgUrl_list[2]
                )
            ]
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(e.__class__.__name__))

    elif len(text_list) >= 4:
        try:
            message = [
                ImageSendMessage(
                    preview_image_url=imgUrl_list[0],
                    original_content_url=imgUrl_list[0]
                ),
                ImageSendMessage(
                    preview_image_url=imgUrl_list[1],
                    original_content_url=imgUrl_list[1]
                ),
                ImageSendMessage(
                    preview_image_url=imgUrl_list[2],
                    original_content_url=imgUrl_list[2]
                ),
                ImageSendMessage(
                    preview_image_url=imgUrl_list[3],
                    original_content_url=imgUrl_list[3]
                )
            ]
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(e.__class__.__name__))

    else:
        message = '目前找不到BOSS耶QQ' 
    
    try:
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(e.__class__.__name__))

def check_other_boss(search_boss):
    """
    【爬蟲】文字輸入功能
    1. 爬 Pokemonhubs 網站
    2. 回傳符合使用者輸入字詞的文章和網址 (str)
    3. 後續在 other 函式中使用
    """ 
    boss_url = 'https://www.pokemonhubs.com/pokemongo/category/legendary-raidboss/'
    current_page = get_page(boss_url)
    contents = []
    while current_page:
        divs1 = current_page.find_all('h2')
        divs2 = current_page.find_all('h3')
        for i in divs1:
            try:
                contents += [{
                    'title': i.text,
                    'url': i.find('a')['href']
                }]
            except:
                pass

        for j in divs2:
            try:
                contents += [{
                    'title': j.text,
                    'url': j.find('a')['href']
                }]
            except:
                pass
        
        try:
            navi_div = current_page.find('div', 'jeg_navigation jeg_pagination jeg_pagenav_1 jeg_aligncenter no_navtext no_pageinfo')
            current_page_url = navi_div.find('a', 'page_nav next')['href']
            current_page = get_page(current_page_url)
        except:
            current_page = False
    
    target = ''
    for article in contents:
        if search_boss in article['title']:
            title = article['title']
            link = article['url']
            target += '・' + title
            target += '\n'
            target += link
            target += '\n\n'
    if len(target) > 0:        
        return target
    else:
        return False

def get_news(event):
    """
    【爬蟲】
    1. 取得寶可夢官方網站 3 篇最新貼文
    2. 回傳使用者: 文章標題、時間、連結
    """
    base_url = 'https://pokemongolive.com'
    post_url = '/zh_hant/post'
    soup = get_page(base_url+post_url)
    articles = soup.find('div', 'grid grid--padded post-list')
    news = ''
    for i in range(3):
        time = articles.select('span')[i].text.strip()
        title = articles.select('a')[i].text.strip()
        url = articles.select('a')[i]['href']
        news += '【'+time+'】\n' + title + '\n' + base_url + url + '\n\n'
        
    try:
        message = [
            TextSendMessage(
                text=news
            )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))

def get_ptt(event):
    """
    【爬蟲】
    1. 取得PokemonGo板近期貼文 (網頁版最新兩頁)
    2. 篩選: 推文數 > 50 且非公告文
    3. 回傳文章標題、時間、連結、推文數
    """
    ptt_url = 'https://www.ptt.cc'
    pokemon_url = '/bbs/PokemonGO/index.html'
    
    # 單頁爬蟲
    def get_article(dom):
        previous_url = dom.select('div a')[7].get('href')
        data = dom.find_all('div', 'r-ent')
        
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

    # 利用單頁爬蟲函式抓多頁 (暫定2頁)
    articles = []
    counter = 0
    current_page = get_page(ptt_url+pokemon_url)
    while counter < 2:
        data, previous_url = get_article(current_page)
        articles += data
        current_page = get_page(ptt_url+previous_url)
        counter += 1

    # 抓 LINE 訊息所需資料
    text = ''
    for article in articles:
        try:
            text += '・' + article['title']
            text += '\n'
            text += article['url']
            text += '\n\n'
        except:
            pass    
    
    try:
        message = [
            TextSendMessage(
                text=text
            )
        ]    
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))

def get_tomchun(event, search_range):
    """
    【爬蟲】
    1. 目標網站: 湯姆群情報站 寶可夢最新資訊
    2. 使用者可自訂爬蟲的網頁頁數 (search_range)
    """
    page_url = 'http://tomchun.tw/tomchun/category/%e5%af%b6%e5%8f%af%e5%a4%a2pokemon-go/page/'
    counter = 1
    target = ''
    while counter <= int(search_range):
        resp = requests.get(page_url+str(counter))
        soup = BeautifulSoup(resp.text, 'html5lib')
        titles = soup.find_all('h2', 'entry-title')
        for t in titles:
            title = t.text
            link = t.find('a')['href']
            target += '・' + title
            target += '\n'
            target += link
            target += '\n\n'
        counter += 1
    
    try:
        message = TextSendMessage(
            text=target
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))

def other(event, text):
    target = check_other_boss(text)
    if target:
        try:
            message = TextSendMessage(
                text=target
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))
    else:
        try:
            message = TextSendMessage(
                text='抱歉! 查無資料'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))

def intro(event):
    text = """【最新消息】
提供最新 3 則官網消息

【團體戰打手】
提供當期頭目的打手攻略

【頭目一覽】
提供當期所有頭目一覽圖

【湯姆】
提供"湯姆群情報站"的最新 5 篇文章

【PTT PokemonGo板近期熱門文章】
提供近期推文數>50的熱門文章

【使用說明】
可以再次看到這串文字使用說明唷~
    """
    try:
        message = TextSendMessage(
            text=text
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))
        