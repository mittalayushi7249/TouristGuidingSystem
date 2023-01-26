from tensorflow import keras
from textblob import TextBlob
from django.conf import settings
path = f'{settings.BASE_DIR}\\analyzer\\'
model = keras.models.load_model(path+'sentiment_analysis.h5')
def isPositive(feedback):

	feedback_polarity = TextBlob(feedback).sentiment.polarity
	#print(feedback_polarity)
	if feedback_polarity>0:
	    print ("Positive")
	    return 1
	else: return 0