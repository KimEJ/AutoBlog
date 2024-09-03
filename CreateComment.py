# from bardapi import BardCookies
import asyncio
import jwt
import logging
import requests
import json

    
class CreateComment:
    def __init__(self, token, id):
        self.room = None
        self.headers = {'Host': 'studio-api.wow.wrtn.ai', "X-Wrtn-Id": id}
        self._refresh_token(token)

    def _refresh_token(self, token):
        with requests.post('https://api.wow.wrtn.ai/auth/refresh', headers={"Refresh": token}) as request:
            response = request.json()
            if response['result'] != "SUCCESS":
                raise Exception("Failed to refresh token")
            decoded = jwt.decode(response['data']['accessToken'], options={"verify_signature": False})

            self.user=decoded["email"]
            self.headers["Authorization"] = "Bearer "+response['data']['accessToken']
            return response['data']['accessToken']
        
    def tool(self, text):
        text = text[:1500]
        with requests.post(url=f'https://studio-api.wow.wrtn.ai/store/tool/65368fcbde87e16e676544df/generate', 
                                     params={'model':'gpt-4', 'platform': 'web', 'user':self.user}, 
                                     json={"inputs": [{"name": "본문", "value": text }],"model": "gpt-4"}, 
                                     headers=self.headers) as request:
            response = request.content
            # data: {"chunk":null}\n\ndata: {"chunk":""}\n\ndata: {"chunk":"I"}\n\ndata: {"chunk":"\'m"}\n\ndata: {"chunk":" sorry"}\n\ndata: {"chunk":","}\n\ndata: {"chunk":" but"}\n\ndata: {"chunk":" I"}\n\ndata: {"chunk":" cannot"}\n\ndata: {"chunk":" generate"}\n\ndata: {"chunk":" a"}\n\ndata: {"chunk":" response"}\n\ndata: {"chunk":" without"}\n\ndata: {"chunk":" a"}\n\ndata: {"chunk":" specific"}\n\ndata: {"chunk":" context"}\n\ndata: {"chunk":" or"}\n\ndata: {"chunk":" user"}\n\ndata: {"chunk":" input"}\n\ndata: {"chunk":"."}\n\ndata: {"chunk":" Please"}\n\ndata: {"chunk":" provide"}\n\ndata: {"chunk":" more"}\n\ndata: {"chunk":" information"}\n\ndata: {"chunk":" or"}\n\ndata: {"chunk":" a"}\n\ndata: {"chunk":" specific"}\n\ndata: {"chunk":" question"}\n\ndata: {"chunk":" for"}\n\ndata: {"chunk":" me"}\n\ndata: {"chunk":" to"}\n\ndata: {"chunk":" answer"}\n\ndata: {"chunk":"."}\n\ndata: {"chunk":""}\n\ndata: {"chunk":null}\n\ndata: {"content":"I\'m sorry, but I cannot generate a response without a specific context or user input. Please provide more information or a specific question for me to answer."}\n\ndata: {"end":"[DONE]"}\n\n
            response = response.decode('utf-8').split('\n')
            matching = [s for s in response if '"content"' in s]
            response = json.loads(matching[0].replace('data: ', ''))

            return response['content']