import requests
from lxml import etree
import os


os.chdir(os.path.dirname(__file__))



class konachan():
    def __init__(self) -> None:
        self.headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
                'Referer':'https://konachan.net/post',
                'Origin':'https://konachan.net'
        }
        self.cookies = {
            'cf_clearance':'FZBRYy11aSIwa0hkEWtoC86VtqNfuycESdOexzFtEh8-1686720133-0-160',
            'country':'CN',
            'blacklisted_tags':'%5B%22%22%5D',
            'konachan.net':'BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTllZjlkZjIyODY0ODNlMzVlZmM3ZjNiY2JkMmM5YmZkBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWF1RTlEN0xNNjZXd2ZBS3JkRVlpUFBzdGhBTTRIU1hkNXlNTUQ4c2xoUG89BjsARg%3D%3D--f1d7b9f6803cb5cecdffaffd96dbf368b4908f29',
            'forum_post_last_read_at':'%222023-06-14T07%3A27%3A48%2B02%3A00%22',
            'vote':'1'
        }
        self.url = 'https://konachan.net/post'
        self.filename = './image/'
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)
        self.pagenum = 0

    def tag_find(self,tag:str,page=0,flag= True):
        filename = self.filename + tag + '/'
        if not os.path.exists(filename):
            os.mkdir(filename)
        param = {
            'page':page,
            'tags':tag
        }
        r = requests.get(url=self.url,headers=self.headers,params=param,cookies=self.cookies)
        if r.status_code == 200:    
            html = etree.HTML(r.text)
            examp_ul_tags = html.xpath('//ul[@id="post-list-posts"]//li/a')
            for a in examp_ul_tags:
                j = a.xpath('@href')[0]
                print(j)
                self.downimage(j,filename,self.pagenum,tag)
                self.pagenum += 1
            if flag:
                pagination = html.xpath('//div[@class= "pagination"]//a/text()')[-2] #总页数
                # pagination = pagination if pagination > 10 else 10
                pagination = int(pagination)
                pagination = pagination if pagination <= 10 else 10
                print(pagination)
                for c in range(pagination-1):
                    self.tag_find(tag,page=2+c,flag=False)
        else:
            print('有问题')
        

    def downimage(self,url:str,filename,i,tag):
        try:
            r = requests.get(url,headers=self.headers,cookies=self.cookies)
            if r.status_code == 200:
                # print(filename+title+uid+'.'+style)
                bum = '000{}'.format(i)
                flag = url.split('.')[-1]
                with open(filename+tag + bum[-4:]+'.'+flag,'wb') as f:
                    f.write(r.content)
                r.close()
            else:
                print(r.status_code,url)
        except Exception as e:
            print("有点问题呢",e)


if __name__ == "__main__":
    a = konachan()
    a.tag_find('lolita_fashion')