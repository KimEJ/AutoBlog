import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import unquote

class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

def croller(blogId="ham_eaten_jellybear", countPerPage=30):
    currentPage = 0
    endOfPage = False
    while not endOfPage:
        # 1. URL
        url = f'https://blog.naver.com/PostTitleListAsync.naver?blogId={blogId}&viewdate=&currentPage={currentPage}&categoryNo=0&parentCategoryNo=0&countPerPage={countPerPage}'

        # 2. URL Request
        response = requests.get(url).text

        # print(response.status_code)

        # 2-1. JSON Parsing
        response = json.loads(response, cls=LazyDecoder)

        total = int(response['totalCount'])
        list = response['postList']

        # 3. Parsing
        for item in list:
            title = unquote(item['title'])
            no = item['logNo']
            print(no)

        # print(f'현재 페이지: {currentPage} / {total // countPerPage + 1}')

        if currentPage * countPerPage >= total:
            endOfPage = True

        # 4. Next Page
        currentPage += 1

if __name__ == "__main__":
    croller()