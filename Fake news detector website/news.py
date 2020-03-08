from newsapi import NewsApiClient
api=NewsApiClient(api_key='932e630a539a47308e1cef5d6eb05ed6')
print(api.get_sources())
