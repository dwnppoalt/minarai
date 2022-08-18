import requests
import os
from urllib.parse import quote_plus
import json
class Wolfram:
    def __init__(self) -> None:
        self.APP_ID = "demo" #REPLACE WITH os.environ["WOLFRAM_APP_ID"]
        self.BASE_API = "https://api.wolframalpha.com/v2/query?input={}&format=image,plaintext&output=JSON&appid={}"
        self.scraper = requests.get
    def parseContent(self, query: str) -> dict:
        url = self.BASE_API.format(query, self.APP_ID)
        response = self.scraper(url).json()

        return response
    
    def filterResults(self, query: str) -> dict:
        query = quote_plus(query)
        obj = self.parseContent(query).get("queryresult")
        if obj.get('pods') == None:
            try:
                items = {"didyoumeans" : obj.get("didyoumeans").get("val")}
            except:
                items = {"didyoumeans" : [i.get('val') for i in obj.get("didyoumeans")]}
        else:
            items =  {
                    "pods" : [
                        {
                            "dataType" : pod.get("title"),
                            "subpods" : [
                                {
                                    'data' : subpod.get("plaintext"),
                                    'alt' : subpod.get("img").get("alt"),
                                    'img' : subpod.get("img").get("src"),

                                } for subpod in pod.get("subpods")
                            ]
                        } for pod in obj.get("pods")

                    ],
                    "didyoumeans" : [i for i in obj.get("didyoumeans")] if obj.get("didyoumeans") else [],
                }
        with open("data.json", "w") as f:
            json.dump(items, f)
        return items
        
    def setAppID(self, appID):
        self.APP_ID = appID
    
