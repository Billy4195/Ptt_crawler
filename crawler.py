import requests
from bs4 import BeautifulSoup as BS
import re
from urllib.request import urlretrieve
import os
import sys

def download_image(articles):
	counts = 0
	for article in articles:
		url = root_url + article['href']
		print(article.text, url)
		res = requests.get(url)
		images = reg_imgur_file.findall(res.text)
		if len(images):
			counts += 1
			store_dir = os.path.join('download' + article.text)
			if not os.path.isdir(store_dir):
				os.mkdir(store_dir)
		for img in set(images):
			ID = re.search('http[s]?://i.imgur.com/(\w+\.(?:jpg|png|gif))',img).group(1)
			if os.path.isfile(ID):
				continue
			file_path = os.path.join(store_dir,ID)
			urlretrieve(img,file_path)
	return counts




def crawler():
	counts = 0
	path = 'https://www.ptt.cc/bbs/Beauty/index.html'
	if not os.path.isdir('download'):
		os.mkdir('download')
	while counts < max_download:
		res = requests.get(path)

		soup = BS(res.text,'html.parser')
		pages =soup.select('div.btn-group-paging a')

		path = root_url + pages[1]['href']
		articles = soup.select('div.title a')
		counts += download_image(articles)
	print('總共下載了{0}篇文章'.format(counts))

reg_imgur_file = re.compile('http[s]?://i.imgur.com/\w+\.(?:jpg|png|gif)')
root_url = 'https://www.ptt.cc'
if len(sys.argv) > 1:
	max_download = sys.argv[1]
else:
	max_download = 10
crawler()