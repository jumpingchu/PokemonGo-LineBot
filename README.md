# Pokemon Go 小幫手

## 使用工具

* Python (含爬蟲 & 資料清理)
* Django
* LINE Bot API
* ngrok (測試)
* Heroku (部署)

## 圖文選單功能

<img src="demo_images/richmenu.jpg" width=400>

* 【最新消息】最新 3 則官網消息

* 【團體戰打手】提供近期頭目的打手攻略圖 (最多顯示 4 個)
		
* 【頭目一覽】提供當期所有頭目一覽圖
		
* 【PokemonGo 板近期熱門文章】提供近期推文數 > 50 的熱門文章
		
* 【湯姆群】提供「湯姆群情報站」的最新五篇文章
		
* 【使用說明】本 LINE Bot 的功能說明

## 文字輸入功能

* **湯姆2**

	* 若不輸入數字預設為 1，例如「湯姆」：顯示 5 篇文章
    * 輸入「湯姆2」: 顯示 10 篇文章
    * 輸入「湯姆3」: 顯示 15 篇文章  ...依此類推
	* **數字前不要空格**

* **其他任何文字**

	* 會先搜尋 Pokemon Hubs 網站的頭目資訊
    * 若無法查到相關資訊，則回傳"抱歉! 查無資料"

## 加入好友

1. ID: @166edspc
		
2. QRcode

<img src="demo_images/166edspc.png" width=200>

## 注意事項

* 由於 Heroku app 會自動休眠，隔一段時間未使用時，第一則訊息回覆時間會較長

## Demo

### 最新消息

<img src="demo_images/news.jpg" width=400>

### 團體戰打手

<img src="demo_images/counter.jpg" width=400>

### 頭目一覽

<img src="demo_images/all_boss.jpg" width=400>

### PokemonGo 板近期熱門文章

<img src="demo_images/ptt.jpg" width=400>

### 湯姆群

<img src="demo_images/tom.jpg" width=400>


## 貢獻

* 歡迎發 Issue 或 PR 提供建議與想法

## 參考網站
* [Pokemon Go 官網](https://pokemongolive.com/post/?hl=zh_hant)
* [Leek Duck](https://leekduck.com)
* [Pokemon Hubs](https://www.pokemonhubs.com)
