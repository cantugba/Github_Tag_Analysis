import requests
from bs4 import BeautifulSoup

result = requests.get("https://api.github.com/search/repositories?q=created%3A2020-09-30..2020-10-31&page=1&per_page=10")
data = result.json()
val = dict()
for repo in data['items']:

       print(repo['name'])
       print(repo['html_url'])
       r = requests.get(repo['html_url'])
       data = r.text
       soup = BeautifulSoup(data,"html.parser")
       table = soup.find('table',{'class':'topic-tag topic-tag-link '})
       print(table)
       print(repo['language'])




# Github-api üzerinden çekilen 'html-url' i kullanarak projelere ulasma ve HTML Tagları arasından veriyi çekme
# Veriyi çekmesi uzun sürüyor
