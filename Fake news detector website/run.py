#from textblob import TextBlob
from newsapi import NewsApiClient 
newsapi=NewsApiClient(api_key='932e630a539a47308e1cef5d6eb05ed6')
#data=newsapi.get_everything(q=s, language='en', page_size=100, sort_by='relevancy')
data = newsapi.get_top_headlines(language='en',country="in", page_size=10)


for i in data['articles']:
    print(i['title'],i['url'])