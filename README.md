# Pokemon Go 小幫手

## 使用工具

* Python (含爬蟲 & 資料清理)
* Django
* LINE Bot API
* ngrok (測試)
* Heroku (部署)

## 功能簡述

### 圖文選單

1. 最新消息

        最新 3 則官網消息
2. 團體戰打手

        提供近期頭目的打手攻略圖 (最多顯示 4 個)
3. 頭目一覽

        提供當期所有頭目一覽圖
4. PokemonGo 板近期熱門文章

        提供近期推文數 > 50 的熱門文章
5. 湯姆群

        提供"湯姆群情報站"的最新五篇文章
6. 使用說明

        本 LINE Bot 的功能說明

### 文字輸入功能

1. 湯姆2

        不輸入數字預設為 1: 顯示 5 篇文章
        輸入"湯姆2": 顯示 10 篇文章 (5*2)
        輸入"湯姆3": 顯示 15 篇文章 (5*3)
        ...依此類推
        (數字前不要空格)

2. 其他任何文字

        會先搜尋 Pokemon Hubs 網站的頭目資訊
        若無法查到相關資訊，則回傳"抱歉! 查無資料"

## Demo

### 自製圖文選單

![richmenu_demo](demo_images/richmenu.jpg)

### 最新消息

![demo1](demo_images/news.jpg)

### 團體戰打手

![demo1](demo_images/counter.jpg)

### 頭目一覽

![demo1](demo_images/all_boss.jpg)

### PokemonGo 板近期熱門文章

![demo1](demo_images/ptt.jpg)

### 湯姆群

![demo1](demo_images/tom.jpg)

---

## 加入好友

1. ID

        @166edspc
2. QRcode

    ![qrcode](demo_images/166edspc.png)

備註：

* 由於 Heroku app 會自動休眠，隔一段時間未使用時，第一則訊息回覆時間會較長

* 歡迎發 issue 或 PR 提供建議與想法
