import urllib.request
import uuid
from PIL import Image
import os

class GetImage:
    def __init__(self, url, path):
        self.url = url
        self.path = path
        self.name = uuid.uuid4().hex
        self.format = self.url.split('.')[-1].split('?')[0]

    def get(self):
        urllib.request.urlretrieve(self.url, f'{self.path}/{self.name}.{self.format}')
        Image.open(f'{self.path}/{self.name}.{self.format}').save(f'{self.path}/{self.name}.webp', 'webp')
        os.remove(f'{self.path}/{self.name}.{self.format}')
        return f'{self.name}.webp'
    
    
if __name__ == "__main__":
    pass