

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pickle



# %% [code]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

data=pd.read_csv('data/latest_dataset.csv')

print(data.head())
#print(data.shape)

from sklearn.model_selection import train_test_split
data = data.dropna()

X_train,X_test,y_train,y_test=train_test_split(data['text'],data['label'],test_size=0.3,random_state=5)
print(X_test.head())
print(X_train.head())


print('Shape of X-Train : ', X_train.shape, '\n',
     'Shape of X-Test : ', X_test.shape, '\n',
     'Shape of Y-Train : ', y_train.shape, '\n',
     'Shape of Y-Test : ', y_test.shape)
#print(X_test[875])
print(X_train)


from sklearn.feature_extraction.text import TfidfVectorizer


tfid=TfidfVectorizer(stop_words='english',max_df=0.7) #Max DOCUMENT FREQUENCY df


transformed_Xtrain=tfid.fit_transform(X_train)
transformed_Xtest=tfid.transform(X_test)
#print(transformed_Xtrain)

from sklearn.linear_model import PassiveAggressiveClassifier

passive=PassiveAggressiveClassifier(max_iter=100)

passive.fit(transformed_Xtrain,y_train)
filename = 'FakeNewsModel.sav'
pickle.dump(passive, open(filename, 'wb'))

from sklearn.metrics import accuracy_score

print(accuracy_score(y_test,passive.predict(transformed_Xtest)))

x_to_predict = pd.Series(np.array(['Unique Creature Captured On Tape In Alaska']))
print(x_to_predict)
print("*****From the Created Model****")
transformed_x_to_predict = tfid.transform(x_to_predict)
#print(passive.predict(transformed_x_to_predict))


pickle.dump(tfid, open('tfid.sav', 'wb'))


loaded_model = pickle.load(open(filename, 'rb'))
print("*****From the Loaded Model****")

print(loaded_model.predict(transformed_x_to_predict))
