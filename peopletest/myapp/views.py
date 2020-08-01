from django.shortcuts import render
from django.http import HttpResponse

# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required

from myapp.models import Person

import json

# Create your views here.
def index(request):
	response = json.dumps([{}])
	return HttpResponse(response, content_type='text/json')

# @csrf_exempt
def addPerson(request):
	if request.method == 'POST':
		#Gets json payload from request
		json_payload = json.loads(request.body)
		#Captures every variable inside json payload
		national_id   = json_payload['national_id']
		name          = json_payload['name']
		last_name     = json_payload['last_name']
		age           = json_payload['age']
		origin_planet = json_payload['origin_planet']
		picture_url   = json_payload['picture_url']
			
		#Create an object with new attributes
		person        = Person(national_id=national_id, name=name, last_name=last_name, age=age, 
								origin_planet=origin_planet, picture_url=picture_url)
			
		try:
			#attempt to save object to DB
			person.save()
			#Confirm object saved
			response = json.dumps([{'Success':'Status 201'}])
		#if any error raises when saving to DB..
		except:
			response = json.dumps([{'Error':'Status 500'}])				

	return HttpResponse(response, content_type='text/json')




def getPeople(request, national_id):
	if request.method == 'GET':
		try:
			#Try to get the person using national_id as key
			human    = Person.objects.get(national_id= national_id)
			response = json.dumps([{'national_id':human.national_id, 'name':human.name, 
									'last_name':human.last_name , 'age':human.age, 
									'origin_planet':human.origin_planet, 'picture_url':human.picture_url}]) 
		except:
			response = json.dumps([{'Error':'Status 404'}])

	return HttpResponse(response, content_type='text/json')


