# Web Resource Crawler

Recursively crawl URL to gather resources such as twitter handle and facebook ids.

### Requirements
- Python 3 & virtualenv
- In order to support crawling SPAs (React, Vue, etc.) you must have the necessary files for Chrome headless.
  - Currently supports windows

### Supports
- Twitter handle
- Facebook page id
- iOS App Store id
- Google Play Store id

### Set up
```
virtualenv venv
source venv/bin/activate (or `\venv\Scripts\activate.bat` in windows)
pip install -r requirements.txt
```

### Quickstart
`python3 cli.py <url>`

Or...

```
from WebResourceCrawler import WebResourceCrawler
crawler = WebResourceCrawler("http://www.zello.com/")
results = crawler.run() # must wait
print(results)

>>> {
    "ios": "508231856",
    "twitter": "Zello",
    "google": "com.loudtalks",
    "facebook": "ZelloMe"
}
```

### Example responses
```
url = https://www.appannie.com/
{
    "twitter": "appannie",
    "facebook": "AppAnnie"
}
```

```
url = http://www.zello.com/
{
    "ios": "508231856",
    "google": "com.loudtalks",
    "twitter": "Zello"
}
```

```
url = http://zynga.com
has multiple twitter handles on the page, but for Twitter and Facebook these are the handles for the company:
{
    "twitter": "zynga",
    "facebook":  "zynga"
}
```