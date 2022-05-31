import grequests
from gevent import monkey
from bs4 import BeautifulSoup
import json
import os
from pathlib import Path
import re


monkey.patch_all()
BASE_DIR = Path(__file__).resolve().parent

class data_generation:

    def __init__(self, BASE_DIR: str):
        self.url = ["https://levistech.ca/Blog"]
        self.DATA_PATH = os.path.join(BASE_DIR, "blogData2.json")

        self.blog = {}
        self.blog["posts"] = []
        self.ID = 1

    def exception_handler(self, request, exception):
        print("Request failed")

    def get_blog_template(self, url):
        try:
            rs=(grequests.get(s_url) for s_url in self.url)
            response = grequests.map(rs, exception_handler=self.exception_handler)
            template = BeautifulSoup(response[0].content, "html.parser")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return template

    def get_number_of_pages(self, template):
        pages = template.findAll("div", {"class": "mfp"})[0]
        pages_list = pages.find_all("a")[2:-2]
        return len(pages_list)

    def create_json_database(self, id, date, title, url, tag):
        try:
            with open(self.DATA_PATH, "w") as f:
                self.blog["posts"].append(
                    {"id": id, "date": date, "title": title, "url": url, "tag": tag}
                )
                json.dump(self.blog, f, indent=2)
        except FileNotFoundError():
            pass
        return

    def curl_data(self):
        """Iterates through all blog posts and appends date, title, url and tags to Json database.
        Date value is gotten with regex that scans for date pattern"""
        template = self.get_blog_template(self.url)
        pages = self.get_number_of_pages(template)
        for page in range(1, pages + 1):
            single_url = self.url[0] + f"?pmpm=(%22443%22:(%22pagPage%22:%22{page}%22))"
            template = self.get_blog_template(single_url)
            results = template.findAll("div", {"class": "mfmcc mfmcc-allBlogs row"})

            for data in range(
                0, len(results[0].findAll("script", type="application/ld+json"))
            ):
                date = re.search(
                    r"[0-9]+-[0-9]+-[0-9]+T",
                    str(results[0].findAll("script", type="application/ld+json")[data]),
                ).group()[:-1]
                title = results[0].findAll("h3", {"class": "bn bn-allBlogs"})[data].text
                url = f"https://levistech.ca{results[0].find_all('a',href=True)[data]['href']}"
                tag = results[0].findAll("div", {"class": "blogCat"})[data].text

                self.create_json_database(
                    id=self.ID, date=date, title=title, url=url, tag=tag
                )
                self.ID += 1
        return


if __name__ == "__main__":
    data = data_generation(BASE_DIR)
    data.curl_data()
