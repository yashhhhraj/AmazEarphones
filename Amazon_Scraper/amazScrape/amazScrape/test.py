import os
import requests


#os.system("scrapy crawl test -o data/data.json")
f = open("C:\\Users\\Yashraj\\Desktop\\Amazon_Scraper\\amazScrape\\amazScrape\\spiders\\data.json", "r+")
url = 'http://13.235.100.194/api/v1/product'
#dd = 
#print(dd)
#print(f)
#xx = requests.post(url, data = f)
#print(xx)
for i in f: 
    print(i)
    x = requests.post(url, data = i, headers={'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmMzU4NDBiZDdlNTk0NGQ4YmE0YTg3MiIsImlhdCI6MTU5NzU3OTE4NCwiZXhwIjoxNjA1MzU1MTg0fQ.T6tgIrZv0L4SAjGZgD_6Rp4OxdQ49JDSG2i13NSQLtg'})
    print(x)