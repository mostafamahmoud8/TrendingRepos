from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
import requests
import itertools

# Create your views here.

#getUrl() used to format the url to specific date and page number
def getUrl(day=30,page=1):
     date = datetime.date.today() - datetime.timedelta(day)
     url = f'https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc&page={page}'

     return url 

#getRepos() used to get first 100 trending Repos in GitHup from specific date until today
def getRepos():
    items = []
    page = 1
    while(len(items)<=100):

        url = getUrl(page=page)
        result = requests.get(url)
        items  = itertools.chain(items,result.json()["items"])
        items  = list(items)
        page  +=1

    return items[0:100]

#SortLanguage to sort the languages based on the number of Repos they used in
def SortLanguage(data):
    for outer in range(len(data)):
        for inner in range(len(data)):
            if data[outer]['count'] > data[inner]['count']:
                data[outer],data[inner] = data[inner],data[outer]
    return data


#GetTrendingLanguage() to represent the result based on the trending programming language 
def GetTrendingLanguage(repos):
    data = []
    for repo in repos:
        found = False
        for item in data:
            if  item['language']==repo['language']:
                item['count'] +=1
                item['repos'].append(repo['html_url'])
                found = True
        if not found:
            language = {
                     'language':repo['language'],
                     'count':1,
                     'repos':[repo['html_url']]
                }
            data.append(language)
             
    return SortLanguage(data)    


        
@api_view(['GET'])
def getTrendRepo(request):
    
    repos = getRepos()
    result =  GetTrendingLanguage(repos)
    return Response(result)