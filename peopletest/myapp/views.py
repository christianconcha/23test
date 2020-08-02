from django.shortcuts import render
from django.http import HttpResponse


from myapp.models import Person
from django.core import serializers

import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger('views.py')

# Create your views here.

def index(request):
	# Index view, displays an empty json:
	response = json.dumps([{}])
	return HttpResponse(response, status= 200,content_type='text/json')




def addPerson(request):
	logger.debug("addPerson")

	if request.method == 'POST' and request.content_type == 'application/json':
		# Gets json payload from request
		json_payload = json.loads(request.body)
		#Captures every variable inside json payload
		national_id   = json_payload['national_id']
		name          = json_payload['name']
		last_name     = json_payload['last_name']
		age           = json_payload['age']
		origin_planet = json_payload['origin_planet']
		picture_url   = json_payload['picture_url']
			
		#Instanciates the class Person to create a person object
		person        = Person(national_id=national_id, name=name, last_name=last_name, age=age, 
								origin_planet=origin_planet, picture_url=picture_url)
			
		try:
			#Attempts to save data to DB
			person.save()
			#Confirms object saved
			response = json.dumps(json_payload)
			status   = 201
		#If any error raises when saving to DB..
		except:
			response = json.dumps([{'Error':'Status 500 INTERNAL SERVER ERROR'}])
			status   = 500
	else:
		response 	 = json.dumps([{'Error':'Status 400 BAD REQUEST'}])
		status 		 = 400
	
	return HttpResponse(response, status=status ,content_type='text/json')




def getPersonById(request, national_id):
	logger.debug("getPersonById")

	if request.method == 'GET':
		try:
			#Try to get a person based on national_id
			person    = Person.objects.get(national_id=national_id)
			response  = json.dumps([{'national_id':person.national_id, 'name':person.name, 
									'last_name':person.last_name , 'age':person.age, 
									'origin_planet':person.origin_planet, 'picture_url':person.picture_url}]) 
			status    = 200
		#If any exception raises when saving to DB..
		except:
			response  = json.dumps([{'Error':'Status 404 NOT FOUND'}])
			status 	  = 404

	return HttpResponse(response, status=status, content_type='text/json')




def getAllPeople(request):
	logger.debug("getAllPeople")

	if request.method=='GET':
		try:
			#Gets everyones records 
			all_people    = Person.objects.all()
			#Creates a json file with all records
			response 	  = serializers.serialize('json',all_people) 
			status 		  = 200
		#If any error raises when saving to DB..
		except:
			response      = json.dumps([{'Error':'Status 500 INTERNAL SERVER ERROR'}])
			status 	  	  = 500			
	
	return HttpResponse(response, status=status, content_type='application/json')	




def updatePerson(request, national_id):
	logger.debug("updatePerson")
	
	if request.method=='PUT' and request.content_type == 'application/json':
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
			person    = Person.objects.get(national_id=national_id)
			# Updates a person based on national_id and a json
			Person.objects.filter(national_id=national_id).update(national_id=nat_id, 
														     	  name=name, last_name=last_name , age=age, 
														     	  origin_planet=origin_planet, picture_url=picture_url)
			response 	 = json.dumps(json_payload)
			status   	 = 200
		except Person.DoesNotExist:
			#If person doesn't exist:
			response 	 = json.dumps([{'Error':'Status 404 NOT FOUND'}])
			status   	 = 404
		finally:
			# On any other errors set status to 500:
			if not response:
				response = json.dumps([{'Error':'Status 500'}])
				status   = 500
	else:
		response 		 = json.dumps([{'Error':'Status 400 BAD REQUEST'}])
		status 		 	 = 400

	return HttpResponse(response, status=status, content_type='text/json')	




def deletePerson(request, national_id):
	logger.debug("deletePerson")

	if request.method=='DELETE':
		try:
			# Looks for a person based on national_id 
			person   = Person.objects.get(national_id=national_id)
			# Updates a person based on national_id and a json
			person.delete()
			response = json.dumps([{'Success':'Status 200 OK'}])
			status   = 200
		except Person.DoesNotExist:
			#If person doesn't exist:
			response = json.dumps([{'Error':'Status 404 NOT FOUND'}])
			status   = 404
		finally:
			# On any other errors set status to 500:
			if not response:
				response = json.dumps([{'Error':'Status 500 INTERNAL SERVER ERROR'}])
				status   = 500

	return HttpResponse(response, status=status, content_type='text/json')	


		





