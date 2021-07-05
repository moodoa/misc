import requests
import pandas as pd
from datetime import datetime

class DPICK:
    def _crawler(self, cookie):
        headers = {"cookie": cookie}
        res = requests.get("https://web.dpick.com/api/v2/posts?popular=true", headers=headers).json()
        articles = []
        before = 0
        keepgoing = True
        while keepgoing:
            if not articles:
                res = requests.get("https://web.dpick.com/api/v2/posts?popular=true", headers=headers).json()
            else:
                print(before)
                res = requests.get(f"https://web.dpick.com/api/v2/posts?before={before}&popular=true", headers=headers).json()  
            if res:
                for info in res:
                    articles.append(f'{info["title"]}\n\nhttps://web.dpick.com/post/{info["id"]}')
                before = res[-1]["id"]
            else:
                keepgoing = False
        for forum in ["keio", "waseda"]:
            res = requests.get(f"https://web.dpick.com/api/v2/forums/{forum}/posts?popular=true", headers=headers).json()
            if res:
                for info in res:
                    articles.append(f'{info["title"]}\n\nhttps://web.dpick.com/post/{info["id"]}')
        return articles
    
    def output(self, cookie):
        articles = self._crawler(cookie)
        series = pd.Series(articles)
        arr = series.values.copy()
        arr.resize(100, len(articles)//100+1)
        data = pd.DataFrame(arr.T)
        data.to_csv(f"{datetime.now().strftime('%Y%m%d')}.csv", encoding="utf-8-sig")
        return "DONE"

if __name__ == "__main__":
    print(" INSERT YOUR COOKIE PLEASE :")
    cookie = input()
    dpick = DPICK()
    dpick.output(cookie)