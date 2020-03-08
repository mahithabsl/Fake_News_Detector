from flask import Flask,render_template
from flask import *
import pickle
import pandas as pd
import numpy as np
from textblob import TextBlob
#nltk.download('punkt')
#nltk.download('brown')
from newsapi import NewsApiClient 
newsapi=NewsApiClient(api_key='932e630a539a47308e1cef5d6eb05ed6')


app=Flask(__name__)
@app.route("/")
def home():
    data = newsapi.get_top_headlines(language='en',country="in", page_size=10)
    l1=[]
    l2=[]
    for i in data['articles']:
        l1.append(i['title'])
        l2.append(i['url'])
    return render_template("home.html",l1=l1,l2=l2)      #template
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/new1")
def new1():
    return render_template("new1.html")    #news predictor
@app.route('/accepted', methods=['GET','POST'])
def accepted():
    if request.method=="POST":
        text1 = request.form['inp']
        tfid=pickle.load(open('model/tfid.sav', 'rb'))
        inpu=text1
        x_to_predict = pd.Series(np.array([inpu]))
        transformed_x_to_predict = tfid.transform(x_to_predict)
        filename = 'model/FakeNewsModel.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        v=loaded_model.predict(transformed_x_to_predict)
        j=v[0]
        if (j=='REAL'):
          text1="NEWS DISPLAYED IS TRUE!!"
        else:
          text1="NEWS DISPLAYED IS FAKE!!"
        txt = inpu
        blob = TextBlob(txt)
        b = blob.noun_phrases
        s = ''
        x=0
        for i in b:
            s = s+ i+" "
            if(x>5):
                break
            x+=1

        data=newsapi.get_everything(q=s, language='en', page_size=10, sort_by='relevancy')
        l1=[]
        l2=[]
        for i in data['articles']:
            l1.append(i['title'])
            l2.append(i['url'])
        
        return render_template("accepted.html",name=text1,sub=inpu,t1=l1,t2=l2)
        

if(__name__)=="__main__":
    app.run(debug=True)