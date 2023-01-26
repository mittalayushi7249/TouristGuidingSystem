# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

# -*- coding: utf-8 -*-
from django.http import HttpResponse

from .models import *
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import login, authenticate,logout
from analyzer.feedback_analysis import isPositive
from django.contrib.auth.hashers import make_password
from .forms import *
# Create your views here.


def getComments(place):

	placeid = Places.objects.all().filter(Name=place)
	
	if(len(placeid)>0):
		placeid = placeid[0].id

		comments = Comments.objects.all().filter(PlaceID=placeid)
		print(comments)

		return comments
	else:
		return False




def top_10_records():

	places = Places.objects.all().order_by('-Ratings')

	if(len(places)>10):
		return places[:10]

	return places


def get_place_type_records(PlaceType):

	places = Places.objects.all().filter(Type=PlaceType).order_by('-Ratings')

	if(len(places)>6):
		return places[:6]

	return places

def get_place_city_records(PlaceCity):

	places = Places.objects.all().filter(City=PlaceCity).order_by('-Ratings')

	if(len(places)>6):
		return places[:6]

	return places


def comments_analyze(place):
	place = Places.objects.all().filter(Name=place)
	
	if(len(place)>0):
		placeid = place[0].id

		comments = Comments.objects.all().filter(PlaceID=placeid)
		total_comments = len(comments)

		comments = Comments.objects.all().filter(PlaceID=placeid).filter(PositveNegative=1)
		positive_comments = len(comments)

		Ratings = (positive_comments*5)//total_comments

		print(Ratings)
		print(placeid)

		Places.objects.filter(id = placeid).update(Ratings = Ratings)

		print("Saved")



def index(request):

	context={}

	context['places'] = top_10_records()


	if request.user.is_authenticated:
		print("looged in ")
		context['loggedin'] = True


	if(request.method=="POST"):
		print("POSt Request")
		options = request.POST.get('options')

		if(options=="city"):
			city = request.POST.get("city")

			places = Places.objects.all().filter(City=city)

			if(places):	

				context['places_city'] = places
				context['City'] = city
			else:
				context['nodata'] = True
			return render(request,'place.html',context)

		elif(options=="place"):
			place = request.POST.get("place")
			places = Places.objects.all().filter(Name=place)

			if(places):	
				place = places[0]
				Ratings = [i for i in range(place.Ratings)]
				context['place'] = place
				context['Ratings'] = Ratings

				comments = getComments(place)
				context['comments']=comments

				

				print(context)

				places = get_place_type_records(place.Type)
				print(places)
				if(places):
					context['PlacesType'] = places
					context['PlaceType'] = place.Type
				else:
					context['PlacesType'] = False

				places = get_place_city_records(place.City)

				if(places):	

					context['PlacesCity'] = places
					context['City'] = place.City
				else:
					context['PlacesCity'] = False



			else:
				context['nodata'] = True

			return render(request,'place.html',context)

	

		message = request.POST.get("comment_message")
		if(message):
			
			place = request.POST.get("hidden_name")
			print(place)
			comments = Comments(UserID=request.user,PlaceID=Places.objects.all().filter(Name=place)[0],Message=message,PositveNegative=isPositive(message))
			comments.save()
			comments_analyze(place)
			context['commentdone'] = True
			print("Comments Send.")
			

	return render(request, 'index.html',context)

def about(request):
	context={}
	if request.user.is_authenticated:
		context['loggedin'] = True

	if(request.method=="POST"):
		print("POSt Request")
		options = request.POST.get('options')

		if(options=="city"):
			city = request.POST.get("city")

			places = Places.objects.all().filter(City=city)

			if(places):	

				context['places_city'] = places
				context['City'] = city

			else:
				context['nodata'] = True
			return render(request,'place.html',context)

		elif(options=="place"):
			place = request.POST.get("place")
			places = Places.objects.all().filter(Name=place)

			if(places):	
				place = places[0]
				Ratings = [i for i in range(place.Ratings)]
				context['place'] = place
				context['Ratings'] = Ratings

				comments = getComments(place)
				context['comments']=comments


				print(context)

				places = get_place_type_records(place.Type)
				print(places)
				if(places):
					context['PlacesType'] = places
					context['PlaceType'] = place.Type
				else:
					context['PlacesType'] = False

				places = get_place_city_records(place.City)

				if(places):	

					context['PlacesCity'] = places
					context['City'] = place.City
				else:
					context['PlacesCity'] = False




			else:
				context['nodata'] = True

			return render(request,'place.html',context)

		message = request.POST.get("comment_message")
		if(message):
			place = request.POST.get("hidden_name")
			comments = Comments(UserID=request.user,PlaceID=Places.objects.all().filter(Name=place),Message=message,PositveNegative=isPositive(message))
			comments.save()
			comments_analyze(place)
			context['commentdone'] = True
			print("Comments Send.")
	
	return render(request,'about.html',context)

def contact(request):


	context={}
	if request.user.is_authenticated:
		context['loggedin'] = True

	if(request.method=="POST"):
		print("POSt Request")
		options = request.POST.get('options')

		if(options=="city"):
			city = request.POST.get("city")

			places = Places.objects.all().filter(City=city)

			if(places):	

				context['places_city'] = places
				context['City'] = city
			else:
				context['nodata'] = True
			return render(request,'place.html',context)

		elif(options=="place"):
			place = request.POST.get("place")
			places = Places.objects.all().filter(Name=place)

			if(places):	
				place = places[0]
				Ratings = [i for i in range(place.Ratings)]
				context['place'] = place
				context['Ratings'] = Ratings

				comments = getComments(place)
				context['comments']=comments


				print(context)

				places = get_place_type_records(place.Type)
				print(places)
				if(places):
					context['PlacesType'] = places
					context['PlaceType'] = place.Type
				else:
					context['PlacesType'] = False

				places = get_place_city_records(place.City)

				if(places):	

					context['PlacesCity'] = places
					context['City'] = place.City
				else:
					context['PlacesCity'] = False


			else:
				context['nodata'] = True

			return render(request,'place.html',context)

		message = request.POST.get("comment_message")
		if(message):
			place = request.POST.get("hidden_name")
			comments = Comments(UserID=request.user,PlaceID=Places.objects.all().filter(Name=place),Message=message,PositveNegative=isPositive(message))
			comments.save()

			comments_analyze(place)


			context['commentdone'] = True
			print("Comments Send.")
	
	return render(request,'contact.html',context)

def place(request):

	context={}
	if request.user.is_authenticated:
		context['loggedin'] = True
	places = Places.objects.all()	
	place = places[0]
	Ratings = [i for i in range(place.Ratings)]
	context['place'] = place
	context['Ratings'] = Ratings


	return render(request,'place.html',context)


def signup(request):
	context={}

	if request.user.is_authenticated:
		context['loggedin'] = True
		return HttpResponseRedirect('/')

	if(request.method=="POST"):


		options = request.POST.get('options')

		if(options=="city"):
			city = request.POST.get("city")

			places = Places.objects.all().filter(City=city)

			if(places):	

				context['places_city'] = places
				context['City'] = city
			else:
				context['nodata'] = True
			return render(request,'place.html',context)

		elif(options=="place"):
			place = request.POST.get("place")
			places = Places.objects.all().filter(Name=place)

			if(places):	
				place = places[0]
				Ratings = [i for i in range(place.Ratings)]
				context['place'] = place
				context['Ratings'] = Ratings


				print(context)

				places = get_place_type_records(place.Type)
				print(places)
				if(places):
					context['PlacesType'] = places
					context['PlaceType'] = place.Type
				else:
					context['PlacesType'] = False

				places = get_place_city_records(place.City)

				if(places):	

					context['PlacesCity'] = places
					context['City'] = place.City
				else:
					context['PlacesCity'] = False



			else:
				context['nodata'] = True

			return render(request,'place.html',context)
		
		name = request.POST.get("signup_name")
		username = request.POST.get("signup_username")
		email = request.POST.get("signup_email")
		password = request.POST.get("signup_password")

		user = User(username=username,email=email,password=make_password(password))
		user.save()
		print("Signed Up Succesfull.")

		context['success'] = True
	



	return render(request,'signup.html',context)



def signin(request):
	context={}

	if request.user.is_authenticated:
		context['loggedin'] = True
		return HttpResponseRedirect('/')


	if(request.method=="POST"):




		options = request.POST.get('options')

		if(options=="city"):
			city = request.POST.get("city")

			places = Places.objects.all().filter(City=city)

			if(places):	

				context['places_city'] = places
				context['City'] = city
			else:
				context['nodata'] = True
			return render(request,'place.html',context)

		elif(options=="place"):
			place = request.POST.get("place")
			places = Places.objects.all().filter(Name=place)

			if(places):	
				place = places[0]
				Ratings = [i for i in range(place.Ratings)]
				context['place'] = place
				context['Ratings'] = Ratings
				print(context)

				places = get_place_type_records(place.Type)
				print(places)
				if(places):
					context['PlacesType'] = places
					context['PlaceType'] = place.Type
				else:
					context['PlacesType'] = False

				places = get_place_city_records(place.City)

				if(places):	

					context['PlacesCity'] = places
					context['City'] = place.City
				else:
					context['PlacesCity'] = False

			else:
				context['nodata'] = True

			return render(request,'place.html',context)




		username = request.POST.get("login_username")
		password = request.POST.get("login_password")

		user = authenticate(username=username, password=password)
		print(user)
		if(user):
			login(request, user)
			return HttpResponseRedirect('/')

		else:
			context['invalid'] = True






	return render(request,'login.html',context)

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


def view_place(request,place):

	print("place"*2,place)


	context={}
	

	if request.user.is_authenticated:
		context['loggedin'] = True


	if(request.method=="POST"):

		message = request.POST.get("comment_message")
		comments = Comments(UserID=request.user,PlaceID=Places.objects.all().filter(Name=place)[0],Message=message,PositveNegative=isPositive(message))
		comments.save()
		comments_analyze(place)
		context['commentdone'] = True
		print("Comments Send.")


	comments = getComments(place)
	context['comments']=comments




	places = Places.objects.all().filter(Name=place)

	if(places):	
		place = places[0]
		Ratings = [i for i in range(place.Ratings)]
		context['place'] = place
		context['Ratings'] = Ratings

		print(context)

		places = get_place_type_records(place.Type)
		print(places)
		if(places):
			context['PlacesType'] = places
			context['PlaceType'] = place.Type
		else:
			context['PlacesType'] = False

		places = get_place_city_records(place.City)

		if(places):	

			context['PlacesCity'] = places
			context['City'] = place.City
		else:
			context['PlacesCity'] = False

	else:
		context['nodata'] = True

	return render(request,'place.html',context)



def feedback(request):

	context={}
	if request.user.is_authenticated:
		print("looged in ")
		context['loggedin'] = True
	else:
		return HttpResponseRedirect('/')

	if(request.method=="POST"):
		print("POSt Request")


		message	= request.POST.get("feedback_message")

		if(message):
			feedback = Feedback(UserID=request.user,Message=message)
			feedback.save()

			context['done'] = True


		options = request.POST.get('options')

		if(options=="city"):
			city = request.POST.get("city")

			places = Places.objects.all().filter(City=city)

			if(places):	

				context['places_city'] = places
				context['City'] = city

			else:
				context['nodata'] = True
			return render(request,'place.html',context)

		elif(options=="place"):
			place = request.POST.get("place")
			places = Places.objects.all().filter(Name=place)

			if(places):	
				place = places[0]
				Ratings = [i for i in range(place.Ratings)]
				context['place'] = place
				context['Ratings'] = Ratings

				comments = getComments(place)
				context['comments']=comments


				print(context)

				places = get_place_type_records(place.Type)
				print(places)
				if(places):
					context['PlacesType'] = places
					context['PlaceType'] = place.Type
				else:
					context['PlacesType'] = False

				places = get_place_city_records(place.City)

				if(places):	

					context['PlacesCity'] = places
					context['City'] = place.City
				else:
					context['PlacesCity'] = False




			else:
				context['nodata'] = True

			return render(request,'place.html',context)

		message = request.POST.get("comment_message")
		if(message):
			place = request.POST.get("hidden_name")
			comments = Comments(UserID=request.user,PlaceID=Places.objects.all().filter(Name=place),Message=message,PositveNegative=isPositive(message))
			comments.save()
			comments_analyze(place)
			context['commentdone'] = True
			print("Comments Send.")


		
	return render(request,'feedback.html',context)