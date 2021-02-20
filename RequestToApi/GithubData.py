import requests

# GET TOPICS

class GithupApi:
    #token için user ve github tokenı ekleyin
    user = None #"cantugba"
    token = None #"2c74cc548500b6d29de6a74b60fc9bbfd459e3cc"
    number = None
    url = None
    datas = None

    def __init__(self,page_number):
        self.user = "cantugba"
        self.token = "2c74cc548500b6d29de6a74b60fc9bbfd459e3cc"
        self.number = page_number
        self.url = "https://api.github.com/search/repositories?q=created%3A2020-11-30..2020-12-31&page="+f"{self.number}"+"&per_page=10"
        self.getData()

    def getData(self):
        headers = {"Accept": "application/vnd.github.mercy-preview+json"}
        repos = requests.get(self.url, headers=headers, auth=(self.user, self.token)).json()
        projects = []
        for repo in repos['items']:
            project = {
                "id": repo["id"],
                "name": repo["name"],
                "url": repo["html_url"],
                "description": repo["description"],
                "topics": repo["topics"]
            }
            projects.append(project)
        self.datas = projects