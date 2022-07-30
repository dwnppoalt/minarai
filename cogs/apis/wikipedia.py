import requests
from urllib.parse import urlencode
import pyshorteners
class Wikipedia:
    def __init__(self) -> None:
        self.BASE_API = "https://en.wikipedia.org/w/api.php?"
        self.scraper = requests
    def parseURL(self, params: dict) -> str:
        return self.BASE_API + urlencode(params)
    def fromQuery(self, query):
        query = query.replace(" ", "_")#&list=&meta=
        params = {"list": "", "meta" : "","titles" : "",'action': 'query', 'format': 'json', 'prop': 'extracts', 'indexpageids': '1', 'generator': 'search', 'exsentences': '2', 'exlimit': 'max', 'exintro': '1', 'explaintext': '1', 'exsectionformat': 'plain', 'gsrsearch': query, 'gsrsort': 'relevance'}
        url = self.parseURL(params)
        print(url)
        jsonify = self.scraper.get(url).json()
        #create a generator that reutrns the value of page id, extract, and title
        dictquery = jsonify.get("query")
        pages = dictquery.get("pages")
        for page in pages:
            pageid = pages.get(page).get("pageid")
            extract = pages.get(page).get("extract")
            title = pages.get(page).get("title")
            yield {
                "pageid" : pageid,
                "extract" : extract,
                "title" : title
            }
    def fromPageID(self, id):
        #url = https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts%7Cpageimages&pageids=271890&exsentences=5&explaintext=1&piprop=thumbnail&pithumbsize=300&pilimit=50&pilicense=any
        params = {"action": "query", "format": "json", "prop": "extracts", "pageids": id, "exsentences": "5", "explaintext": "1"}
        imgparams = {"action": "query", "format": "json", "prop": "pageimages", "pageids": id, "piprop": "thumbnail", "pithumbsize": "300", "pilicense": "any"}
        imgurl = self.parseURL(imgparams)
        url = self.parseURL(params)
        jsonify = self.scraper.get(url).json()
        pages = jsonify.get("query").get("pages")
        imgjsonify = self.scraper.get(imgurl).json()
        for page in pages:
            extract = pages.get(page).get("extract")
            title = pages.get(page).get("title")
            pageid = pages.get(page).get("pageid")
            img = imgjsonify.get("query").get("pages").get(str(page)).get("thumbnail").get("source")
            yield {
                "pageid" : pageid,
                "extract" : extract,
                "title" : title,
                "thumbnail" : img
            }
    
    def dlPDF(self, title):
        ddl = "https://en.wikipedia.org/api/rest_v1/page/pdf/{}".format(title)
        shortener = pyshorteners.Shortener()
        return shortener.tinyurl.short(ddl)



    