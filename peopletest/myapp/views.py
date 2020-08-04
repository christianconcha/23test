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
	# Index view. It displays all path available :
	response = json.dumps([{'Creates a person based on a json':'/post/people', 
							'Retrieves a person by their national_id':'/get/people/"national_id"',
							'Retrieves all data in DB':'/get/people',
							'Updates a person data by their national_id':'/put/people/"national_id"',
							'Deletes a person by national_id':'/delete/people/"national_id"'
							}])
	return HttpResponse(response, status= 200, content_type='application/json')




def addPerson(request):
	logger.debug("addPerson")

	if request.method == 'POST' and request.content_type == 'application/json':
		# Gets json payload from request
		json_payload = json.loads(request.body)
		#Captures every variable contained in json payload
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
			# Setup http status code
			status   = 201
		#If any error raises when saving to DB..
		except:
			response = json.dumps([{'Error':'Status 500 INTERNAL SERVER ERROR'}])
			# Setup http status code
			status   = 500
	else:
		response 	 = json.dumps([{'Error':'Status 400 BAD REQUEST'}])
		# Setup http status code
		status 		 = 400
	
	return HttpResponse(response, status=status, content_type='application/json')




def getPersonById(request, national_id):
	logger.debug("getPersonById")

	if request.method == 'GET':
		try:
			#Try to get a person based on national_id
			person    = Person.objects.get(national_id=national_id)
			response  = json.dumps([{'national_id':person.national_id, 'name':person.name, 
									'last_name':person.last_name , 'age':person.age, 
									'origin_planet':person.origin_planet, 'picture_url':person.picture_url}]) 
			# Setup http status code
			status    = 200
		#If any exception raises when saving to DB..
		except:
			response  = json.dumps([{'Error':'Status 404 NOT FOUND'}])
			# Setup http status code
			status 	  = 404

	return HttpResponse(response, status=status, content_type='application/json')




def getAllPeople(request):
	logger.debug("getAllPeople")

	if request.method=='GET':
		try:
			#Gets everyone's records 
			all_people    = Person.objects.all()
			#Serializes a json with all records
			response 	  = serializers.serialize('json',all_people) 
			# Setup http status code
			status 		  = 200
		#If any error raises when saving to DB..
		except:
			response      = json.dumps([{'Error':'Status 500 INTERNAL SERVER ERROR'}])
			# Setup http status code
			status 	  	  = 500			
	
	return HttpResponse(response, status=status, content_type='application/json')	




def updatePerson(request, national_id):
	logger.debug("updatePerson")

	response=[]
	
	if request.method=='PUT' and request.content_type == 'application/json':
		# Gets json payload from request
		json_payload  = json.loads(request.body)
		#Captures every variable contained in Json payload
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
			# Setup http status code
			status   	 = 200

		except Person.DoesNotExist:
			#If person doesn't exist:
			response 	 = json.dumps([{'Error':'Status 404 NOT FOUND'}])
			# Setup http status code
			status   	 = 404
		except:
			# On any other errors set status to 500:
			if not response:
				response = json.dumps([{'Error':'Status 500 INTERNAL SERVER ERROR'}])
				# Setup http status code
				status   = 500
	else:
		response 		 = json.dumps([{'Error':'Status 400 BAD REQUEST'}])
		# Setup http status code
		status 		 	 = 400

	return HttpResponse(response, status=status, content_type='application/json')	




def deletePerson(request, national_id):
	logger.debug("deletePerson")

	response = []
	if request.method=='DELETE':
		try:
			# Looks for a person based on national_id 
			person   = Person.objects.get(national_id=national_id)
			# Deletes a person based on national_id and a json
			person.delete()
			response = json.dumps([{'Success':'Status 200 OK'}])
			# Setup http status code
			status   = 200
		except Person.DoesNotExist:
			#If person doesn't exist:
			response = json.dumps([{'Error':'Status 404 NOT FOUND'}])
			# Setup http status code
			status   = 404
		except:
			# On any other errors set status to 500:
			if not response:
				response = json.dumps([{'Error':'Status 500 INTERNAL SERVER ERROR'}])
				# Setup http status code
				status   = 500

	return HttpResponse(response, status=status, content_type='application/json')	


		





