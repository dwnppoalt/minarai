
import requests
from bs4 import BeautifulSoup
class Books:
    def __init__(self):
        self.url = "http://gen.lib.rus.ec/search.php?req={}&column=title"
        self.mirror1 = "http://library.lol/main/{}"
        self.mirror2 = "http://libgen.rocks/ads.php?md5={}"
        self.MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io", "Infura"]
        self.col_names = [
        "ID",
        "Author",
        "Title",
        "Publisher",
        "Year",
        "Pages",
        "Language",
        "Size",
        "Extension",
        "Mirror_1",
        "Mirror_2",
        "Mirror_3",
        "Mirror_4",
        "Mirror_5",
        "Edit",
    ]
    def get_book(self, book):
        book = "%20".join(book.split(" "))
        url = (self.url.format(book))
        book_page = requests.get(url)
        soup = BeautifulSoup(book_page.text, "lxml")
        for subheading in soup.find_all("i"):
            subheading.decompose()
        information_table = soup.find_all("table")[2]

        raw_data = [
            [
                td.a["href"]
                if td.find("a")
                and td.find("a").has_attr("title")
                and td.find("a")["title"] != ""
                else "".join(td.stripped_strings)
                for td in row.find_all("td")
            ]
            for row in information_table.find_all("tr")[1:] 
        ]

        output_data = [dict(zip(self.col_names, row)) for row in raw_data]
        return output_data
    def download(self, md5):
        url = (self.mirror1.format(md5))
        book_page = requests.get(url)
        source = ""
        base_url = "https://library.lol"
        if book_page.status_code != 200:
            url = (self.mirror2.format(md5))
            book_page = requests.get(url)
            source = "https://libgen.rocks/"
            base_url = "https://libgen.rocks"
            if book_page.status_code != 200:
                return None
        soup = BeautifulSoup(book_page.text, "lxml")
        URLS = soup.find_all("a", string=self.MIRROR_SOURCES)
        download_links = {link.string: source + link["href"] for link in URLS}
        img = soup.find("img").get("src")
        download_links["Image"] = base_url + img
        download_links["Title"] = soup.find("h1").text
        return download_links

