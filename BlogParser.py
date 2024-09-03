from typing import Any
import requests
from bs4 import BeautifulSoup
import re
import datetime

import CreateComment


def ask_wrtn(text):
    id='W1.3.2501006464537361200005373612000051067170724.vLjb5-cPJxRlsTO6t35hp.1702960711751'
    token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0NjhkM2FhMTU5N2UzNWRiN2QzYmVjMCIsImlhdCI6MTcwMjk2MDczNCwiZXhwIjoxNzA0MTcwMzM0fQ.OAmVj_ZkJwAiXJL26dvGGg8QOmM0NDPJ_P0sEQsOOZQ'
    create_comment = CreateComment.CreateComment(token, id)
    comment = create_comment.tool(text)
    return comment
        

class BlogParser:
    def __init__(self, log_no):
        self.log_no = log_no
        self.user = 'ham_eaten_jellybear'
        self.soup = None
        self.src_url = f'https://m.blog.naver.com/{self.user}/{self.log_no}'
        self.title = None
        self.text = None
        self.tag_list = []
        self.timestamp = None
        self.image = None

    def parse(self):
        # self.get_src_url(f'https://m.blog.naver.com/{self.user}/{self.log_no}')
        self.get_blog()
        self.title_scrapping(self.src_url)
        self.text_scrapping(self.src_url)
        self.tag_scrapping(self.src_url)
        self.timestamp_scrapping(self.src_url)
        self.image_scrapping()
        return self.title, self.text, self.tag_list, self.timestamp, self.image

    def get_blog(self):
        response = requests.get(self.src_url)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'lxml')
        return self.soup
    
    def get_src_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        self.src_url = "https://blog.naver.com" + soup.iframe['src']
        return self.src_url
    
    def title_scrapping(self, url):
        
        self.title = self.soup.find('meta', {'property': 'og:title'})['content']
        return self.title

    def text_scrapping(self, url):
        soup = self.soup.find('div', {'class': 'se-main-container'})

        if soup:
            text = soup.get_text()
            text = text.replace('\n', '')
        else:
            text = "None"
        self.text = text
        return text
    
    def tag_scrapping(self, url):
        tags = self.soup.find('div', {'class': 'post_tag'})
        if tags:
            tags = tags.find_all('span', {'class': 'ell'})
            
            for tag in tags:
                self.tag_list.append(tag.get_text().replace('#', ''))
            return self.tag_list
        else:
            return []
        
    def timestamp_scrapping(self, url):
        try:
            self.timestamp = self.soup.find('p', {'class': 'blog_date'}).get_text()
            if self.timestamp.find('전') != -1:
                self.timestamp = datetime.datetime.now().strftime('%Y. %m. %d')
        except AttributeError:
            self.timestamp = datetime.datetime.now().strftime('%Y. %m. %d')
        return self.timestamp
    
    def image_scrapping(self):
        self.image = self.soup.find('meta', {'property': 'og:image'})['content']
    
if __name__ == "__main__":
    blogParser = BlogParser('223267393930')
    title, text, tag, timestamp, image = blogParser.parse()
    comment = ask_wrtn(text)

    print(comment)