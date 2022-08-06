import requests
import os
class Wolfram:
    def __init__(self) -> None:
        self.APP_ID = os.environ["WOLFRAM_APP_ID"]
        self.BASE_API = "https://api.wolframalpha.com/v2/query?input={}&format=image,plaintext&output=JSON&appid={}"
        self.scraper = requests.get
    def parseContent(self, query: str) -> dict:
        url = self.BASE_API.format(query, self.APP_ID)
        response = self.scraper(url).json()

        return response
    
    def filterResults(self, query: str) -> dict:
        query = query.replace(" ", "%2B")
        obj = self.parseContent(query).get("queryresult")
        if obj.get('success') != True:
            raise Exception("Query failed")
        
        return {
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
                ]
            }
        
    def setAppID(self, appID):
        self.APP_ID = appID
    

