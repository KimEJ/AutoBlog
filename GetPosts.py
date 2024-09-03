import json
import requests
import re

class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)
    
class GetPosts:
    def __init__(self, blogId="ham_eaten_jellybear", countPerPage=30):
        self.blogId = blogId
        self.countPerPage = countPerPage
        self.currentPage = 1
        self.endOfPage = False
        self.total = 0
        self.list = []
        
    def get(self):
        url = f'https://blog.naver.com/PostTitleListAsync.naver?blogId={self.blogId}&viewdate=&currentPage={self.currentPage}&categoryNo=0&parentCategoryNo=0&countPerPage={self.countPerPage}'
        response = requests.get(url).text
        response = json.loads(response, cls=LazyDecoder)
        self.total = int(response['totalCount'])
        self.list += response['postList']
        return self.list
    
    def next(self):
        self.currentPage += 1
        if self.currentPage * self.countPerPage >= self.total:
            self.endOfPage = True
        return self.endOfPage
    
    def reset(self):
        self.currentPage = 1
        self.endOfPage = False
        self.total = 0
        self.list = []
        
    def get_all(self):
        self.get()
        print(f'총 {self.total}개의 글이 있습니다. {len(self.list)}개의 글을 가져왔습니다.')
        while not self.endOfPage:
            self.next()
            print(f'현재 페이지: {self.currentPage} / {self.total // self.countPerPage + 1}')
            print("=============================================\n")
            self.get()
            print(f'총 {self.total}개의 글이 있습니다. {len(self.list)}개의 글을 가져왔습니다.')
        return self.list
    
if __name__ == "__main__":
    getPosts = GetPosts()
    lists = getPosts.get_all()
    print(lists)