import gensim.models.keyedvectors as word2vec #need to use due to depreceated model
from nltk.tokenize import RegexpTokenizer

from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.layers import LSTM, Conv1D, Dense, Flatten, MaxPooling1D, Dropout

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve,  roc_auc_score, classification_report



#read CSV file containing tweets and labels, using Pandas , to get a dataframe
tweetsData = pd.read_csv('Sentiment Analysis Dataset.csv', skiprows=[8835],nrows=40000) #skiping these two rows as they have some bad data
tweetsData.head()

#Dividing the dataset into features and lables
tweets = tweetsData['SentimentText']
labels = tweetsData['Sentiment']

#check the distribution of lebels
labels_count = labels.value_counts()
labels_count.plot(kind="bar")
print("Values Counts ", labels.value_counts())

#Looks like the distribution is even

#Lower and split the dialog
#and use regular expression to keep only letters we will use nltk Regular expression package
tkr = RegexpTokenizer('[a-zA-Z@]+')

tweets_split = []

for i, line in enumerate(tweets):
    #print(line)
    tweet = str(line).lower().split()
    tweet = tkr.tokenize(str(tweet))
    tweets_split.append(tweet)

print("tweets split",tweets_split[1])

'''
Use pretrained Word2Vec model from google but trim the word list to 50,000 compared to 3,000,000 in the original
Google pretrained model
'''

w2vModel = word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True, limit=50000)

#Convert words to integers
tokenizer = Tokenizer(num_words=len(tweets_split)+1)
tokenizer.fit_on_texts(tweets_split)
X = tokenizer.texts_to_sequences(tweets_split)

#length of tweet to consider
maxlentweet = 30
#add padding
X = pad_sequences(X, maxlen=maxlentweet)
print("X _ shape", X.shape)

#create a embedding layer using Google pre triained word2vec (50000 words)
embedding_layer = Embedding(input_dim=w2vModel.syn0.shape[0], output_dim=w2vModel.syn0.shape[1], weights=[w2vModel.syn0],
                            input_length=X.shape[1]+1)

#create model combining LSTM with 1D Convonutional layer and MaxPool layer

lstm_out = 150

model = Sequential()
model.add(embedding_layer)
model.add(Conv1D(filters=64, kernel_size=5, activation='relu', padding='causal'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.7))
model.add(LSTM(units=lstm_out))
model.add(Dropout(0.7))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])




#split dataset 90:10
#X_train : training data - features
#Y_train : training data - labels
X_train, X_test, Y_train, Y_test = train_test_split(X, labels, test_size= 0.1, random_state = 24)

#fit model
batch_size = 32
training = model.fit(X_train, Y_train, epochs=5, verbose=1, batch_size=batch_size)
print(model.summary())

#analyze the results
score, acc = model.evaluate(X_test, Y_test, verbose = 2, batch_size=batch_size)
y_pred = model.predict(X_test)



#Other accuracy metrices y_pred = (y_pred > 0.5) #confusion metrix cm = confusion_matrix(Y_test, y_pred) print(cm)
#F1 Score, Recall and Precision
print(classification_report(Y_test, y_pred, target_names=['Positive', 'Negative']))
model.save('sentiment_analysis.h5')
