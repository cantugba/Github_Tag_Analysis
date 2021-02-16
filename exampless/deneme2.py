import json
import requests
from bs4 import BeautifulSoup

user = "tugbaca"
token = "2c74cc548500b6d29de6a74b60fc9bbfd459e3cc"
result = requests.get("https://api.github.com/search/repositories?q=created%3A2020-09-30..2020-10-31&page=1&per_page=10")
data = result.json()
val = dict()
for repo in data['items']:
    #yorum satırları web kazıma ->souplar
       # print(repo['name'])
       # print(repo['html_url'])
       val = repo['html_url']
       # r  = requests.get(repo['html_url'])
       # data = r.text
       # soup = BeautifulSoup(data,"html.parser")
       # table = soup.find('table',{'class':'topic-tag topic-tag-link '})
       # print(table)
       # print(repo['language'])



       # #
       # r = requests.get("https://github.com/Vishruth-S/CompetitiveCode")
       # data = r.text
       # soup = BeautifulSoup(data, "html.parser")
       # table = soup.find('table', {'class': 'topic-tag topic-tag-link '})
       # print(table)
       #print("vals",val)

#https://medium.com/swlh/build-a-dynamic-portfolio-with-the-github-api-6d74081e5164
numb = 50
url = "https://api.github.com/search/repositories?q=created%3A2020-09-30..2020-10-31&page="+f"{numb}"+"&per_page=10"
headers = {"Accept": "application/vnd.github.mercy-preview+json"}
repos = requests.get(url, headers=headers, auth=(user, token)).json()

projects = []

for repo in repos['items']:
       #if repo["homepage"]:
       project = {
                     #"id": repo["id"],
                     "name": repo["name"],
                     #"url": repo["html_url"],
                     #"description": repo["description"],
                     "topics": repo["topics"],
                     #"images": repo["homepage"].split(";")
              }
       projects.append(project)
numb+=1
print(numb)
print(projects)