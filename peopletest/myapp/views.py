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
	# Creates a non-empty response 
	response = json.dumps([{"Error":"getPersonById"}])

	if request.method == 'GET':
		try:
			#Try to get the person using national_id as key
			person    = Person.objects.get(national_id=national_id)
			response  = json.dumps([{'national_id':person.national_id, 'name':person.name, 
									'last_name':person.last_name , 'age':person.age, 
									'origin_planet':person.origin_planet, 'picture_url':person.picture_url}]) 
		#If any error raises when saving to DB..
		except:
			response  = json.dumps([{'Error':'Status 404'}])

	return HttpResponse(response, content_type='text/json')



def getAllPeople(request):
	logger.debug("Entrando a getAllPeople")
	# Creates a non-empty response 
	response = json.dumps([{"Error":"getAllPeople"}])
	print("PASANDO POR AQUI11111111")

	if request.method=='GET':
		try:
			print("PASANDO POR AQUI")
			#Gets everyones records on DB
			all_people    = Person.objects.all()
			#Creates a json file with all records
			response 	  = serializers.serialize('json',all_people) 
		#If any error raises when saving to DB..
		except:
			response      = json.dumps([{'Error':'Status 404 en getAllPeople'}])
	
	return HttpResponse(response, content_type='application/json')	


def updatePerson(request):
	pass






