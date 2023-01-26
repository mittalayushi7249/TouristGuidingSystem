from tensorflow import keras
from textblob import TextBlob
model = keras.models.load_model('sentiment_analysis.h5')
feedback = input("Enter :")

feedback_polarity = TextBlob(feedback).sentiment.polarity
if feedback_polarity>0:
    print ("Positive")
else: print ("negative")