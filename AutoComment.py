#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 10:57
# @Author  : Arrow and Bullet
# @Software: PyCharm
# @Function:
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

def delete_iframe(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    src_url = "https://blog.naver.com" + soup.iframe['src']
    return src_url
def title_scrapping(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('meta', {'property': 'og:title'})['content']
    return title

def text_scrapping(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    soup = soup.find('div', {'class': 'se-main-container'})

    if soup:
        text = soup.get_text()
        text = text.replace('\n', '')
    else:
        text = "None"

    return text

async def create_comment(text):
    bot = await Chatbot.create(cookies=cookies) # Passing cookies is "optional", as explained above
    text = "다음 글에 적절한 댓글을 만들어 주세요:\n"+text
    # print(title)
    # print(text)

    response = await bot.ask(prompt=text, conversation_style=ConversationStyle.creative)
    response = response['item']['messages']

    comment = ""
    for message in response:
        if message['author'] == 'bot':
            comment += message['text'] + "\n"

    await bot.close()
    return comment

df = pd.read_excel('./test.xlsx', sheet_name='Sheet1')
urls = list(df['URL'])

import asyncio
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
cookies = json.loads(open("./bing_cookies_test.json", encoding="utf-8").read())  # might omit cookies option

async def main(url):
    
    print(url)
    src_url = delete_iframe(url)
    # title = title_scrapping(src_url)
    text = text_scrapping(src_url)

    if text == "None":
        print(url+" is None")
    else:
        comment = await create_comment(text)
        print(comment)
        print("=============================================\n")
        
        # write xlsx
        df.loc[df['URL'] == url, 'comment'] = comment
        df.to_excel('./output.xlsx', sheet_name='Sheet1', index=False)
        print("write xlsx success")
        print("=============================================\n")

if __name__ == "__main__":
    futures = [asyncio.ensure_future(main(url)) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))
    loop.close()
    print("\n\nAll tasks finished")
