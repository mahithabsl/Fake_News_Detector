from bot import telegram_chatbot
import numpy as np
import pickle
import pandas as pd
from textblob import TextBlob
from newsapi import NewsApiClient

fake_news = {
    'A letter providing tips on how to protect against the new coronavirus was authored by pathologist James Robb.':'https://www.snopes.com/fact-check/zinc-lozenges-coronavirus/',
    'In February 2020 the Vatican said that Pope Francis and two aides had tested positive for COVID-19, a disease caused by a new coronavirus.':'https://www.snopes.com/fact-check/pope-francis-coronavirus/',
    'NASA warned that Asteroid 52768 (1998 OR2) could hit Earth in April 2020 and cause catastrophic danger.':'https://www.snopes.com/fact-check/asteroid-warning-april-2020/',
    'The BBC reported in February 2020 that Quaden Bayles had committed suicide.':'https://www.snopes.com/fact-check/quaden-bayles-suicide-hoax/'

}

#from sklearn.feature_extraction.text import TfidfVectorizer
tfid = pickle.load(open('tfid.sav', 'rb'))
x_to_predict = pd.Series(np.array(['Hey']))
filename = 'FakeNewsModel.sav'
loaded_model = pickle.load(open(filename, 'rb'))

bot = telegram_chatbot("config.cfg")


def newsFetcher(txt, top = False):

    newsapi = NewsApiClient(api_key='932e630a539a47308e1cef5d6eb05ed6')
    if top:
        data = newsapi.get_top_headlines(language='en',sources='bbc-news,the-verge')
        hash = dict()
        for i in data['articles']:
            if i['title'] not in hash.keys():
                hash[i['title']] = i['url']
        return hash



    blob = TextBlob(txt)
    b = blob.noun_phrases
    s = ''
    x = 0
    for i in b:
        s = s + i + " "
        if (x > 5):
            break
        x += 1
    data = newsapi.get_everything(q=s, language='en', page_size=100, sort_by='relevancy')
    hash = dict()
    for i in data['articles']:
        if i['title'] not in hash.keys():
            hash[i['title']] = i['url']
    return hash



def checkNewsInModel(message, tfid = tfid, loaded_model = loaded_model):
    print(message)


    x_to_predict = pd.Series(np.array([message]))

    transformed_x_to_predict = tfid.transform(x_to_predict)

    res = loaded_model.predict(transformed_x_to_predict)

    if res[0] == 'REAL':
        print('Real')
        return 'Your news is Real!👍'
    else:
        print('fake')
        return 'Beware! This seems Fake!'




def make_reply(msg):
    reply = None
    reply = 'okay'
    return reply


update_id = None
while True:
    updates = bot.get_updates(offset=update_id)


    updates = updates["result"]
    #updates = None
    if updates:


        
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            try:
                message = message.lower()
            except:
                message = 'hi'

            print('msg', message)
            from_ = item["message"]["from"]["id"]
            greetings = ['hi','yo', 'wassup', 'sup', 'hey', 'hello','namaste','👋']
            if message.lower() in greetings:
                reply = "Hello I'm Fake News Detector bot🤖\n \n1) Want to verify some news?🗞\ntype: 'Verify News'\n2) Want to know current news?🗞\ntype: 'Get News'\n3) Want to see top fake news?🗞\ntype: 'Get Fake News'"
            elif message.lower() in ['verify news', 'verify']:
                bot.send_message("Okay, I'm waiting.", from_)
                updates = bot.get_updates(offset=update_id)
                updates = updates["result"]
                if updates:
                    for item in updates:
                        update_id = item["update_id"]
                        try:
                            message = str(item["message"]["text"])
                        except:
                            message = None
                        from_ = item["message"]["from"]["id"]
                        reply = checkNewsInModel(message)
                        bot.send_message(reply, from_)
                        prev = message
                        bot.send_message('Would you like to read more news related to your search?', from_)
                        updates = bot.get_updates(offset=update_id)
                        updates = updates["result"]
                        if updates:
                            for item in updates:
                                update_id = item["update_id"]
                                try:
                                    message = str(item["message"]["text"])
                                except:
                                    message = None
                        if message.lower() == 'yes':
                            h = newsFetcher(prev)
                            c = 0
                            for i in h.keys():
                                c += 1
                                if c > 5:
                                    break
                                bot.send_message(str(i) + '\n' + str(h[i]), from_)
                            reply = 'Read on! :)'
                        else:
                            reply = 'Okay :)'

            elif message.lower() == 'get news':
                reply = "Here's a list of latest news articles:"
                bot.send_message(reply, from_)
                h = newsFetcher(message, top = True)
                c = 0
                for i in h.keys():
                    c += 1
                    if c>5:
                        break
                    bot.send_message(str(i)+'\n'+str(h[i]), from_)
                reply = 'Read on! :)'
            elif message.lower() == 'get fake news':
                for i in fake_news.keys():
                    bot.send_message(str(i) + '\n' + str(fake_news[i]), from_)
                reply = 'Read on! :)'

            elif message == '/start':
                reply = 'starting...'



            else:
                reply ="I don't understand your command."






            #reply = checkNewsInModel(message)

            bot.send_message(reply, from_)
