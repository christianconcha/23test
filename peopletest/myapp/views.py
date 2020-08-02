from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf   import csrf_exempt
# from django.contrib.auth.decorators import login_required

from myapp.models import Person
from django.core import serializers

import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger('views.py')
# Create your views here.
# def index(request):
# 	response = json.dumps([{}])
# 	return HttpResponse(response, content_type='text/json')

# @csrf_exempt
# @login_required
def addPerson(request):
	logger.debug("addPerson")
	# Creates a non-empty response 
	response = json.dumps([{"Error":"addPerson"}])

	if request.method == 'POST':
		# Gets json payload from request
		json_payload = json.loads(request.body)
		#Captures every variable inside json payload
		national_id   = json_payload['national_id']
		name          = json_payload['name']
		last_name     = json_payload['last_name']
		age           = json_payload['age']
		origin_planet = json_payload['origin_planet']
		picture_url   = json_payload['picture_url']
			
		#Instanciates an object with attributes
		person        = Person(national_id=national_id, name=name, last_name=last_name, age=age, 
								origin_planet=origin_planet, picture_url=picture_url)
			
		try:
			#Attempts to save data to DB
			person.save()
			#Confirms object saved
			response = json.dumps([{'Success':'Status 201'}])
		#If any error raises when saving to DB..
		except:
			response = json.dumps([{'Error':'Status 500'}])
	
	return HttpResponse(response, content_type='text/json')



def getPersonById(request, national_id):
	logger.debug("Entrando a getPersonById")
	# Creates a non-empty response 
	response = json.dumps([{"Error":"getPersonById"}])

	if request.method == 'GET':
		try:
			#Try to get a person based on national_id
			person    = Person.objects.get(national_id=national_id)
			response  = json.dumps([{'national_id':person.national_id, 'name':person.name, 
									'last_name':person.last_name , 'age':person.age, 
									'origin_planet':person.origin_planet, 'picture_url':person.picture_url}]) 
		#If any error raises when saving to DB..
		except:
			response  = json.dumps([{'Error':'Status 404'}])

	return HttpResponse(response, content_type='text/json')



def getAllPeople(request):
	logger.debug("getAllPeople")
	# Creates a non-empty response 
	response = json.dumps([{"Error":"getAllPeople"}])

	if request.method=='GET':
		try:
			#Gets everyones records 
			all_people    = Person.objects.all()
			#Creates a json file with all records
			response 	  = serializers.serialize('json',all_people) 
		#If any error raises when saving to DB..
		except:
			response      = json.dumps([{'Error':'Status 404'}])
	
	return HttpResponse(response, content_type='application/json')	


def updatePerson(request, national_id):
	logger.debug("updatePerson")
	# Creates a non-empty response 
	response = json.dumps([{"Error":"updatePerson"}])
	
	if request.method=='PUT':
		# Gets json payload from request
		json_payload  = json.loads(request.body)
		#Captures every variable inside Json payload
		nat_id        = json_payload['national_id']
		name          = json_payload['name']
		last_name     = json_payload['last_name']
		age           = json_payload['age']
		origin_planet = json_payload['origin_planet']
		picture_url   = json_payload['picture_url']

		try:
			# Looks for a person based on national_id 
			person       = Person.objects.get(national_id=national_id)
			if person:
				# Updates a person based on national_id and a json
				Person.objects.filter(national_id=national_id).update(national_id=nat_id, 
															     	  name=name, last_name=last_name , age=age, 
															     	  origin_planet=origin_planet, picture_url=picture_url)
				response = json.dumps([{'Success':'Status 200'}])
			else:
				response = json.dumps([{'Error':'Status 404'}])	
		except:
			response     = json.dumps([{'Error':'Status 500'}])

	return HttpResponse(response, content_type='text/json')	


def deletePerson(request, national_id):
	pass




