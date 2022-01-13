import requests
from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets, status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.core import serializers
import json
from .serializers import *

from .Helpers import Helpers
from .constant.ApiUrl import ApiUrl
from .constant.ErrorMessages import ErrorMessages
from .constant.JsonKey import JsonKey
from .models import UserProfile, Error, Countries, Histories, Types, Fact


@csrf_exempt
@api_view(['GET', 'POST'])
def registration(request):
    errors = Error()
    params = request.data
    print(params)

    login = params.get('login')
    password = params.get('password')
    country_id = params.get('country_id')

    if request.method == 'POST':
        print("POST")

        if (login == None or password == None or country_id == None):
            errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)

        country = Countries.objects.get(id=country_id)

        try:
            UserProfile.objects.get(login=login, password=password)
            print("NOT ERROR EXIST")
            # Если есть зареганый аккаунт, то сработает этот сценарий
            errors.append(ErrorMessages.REGISTRATION_ERROR_400)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            pass

        user = UserProfile.objects.create(login=login, password=password, country=country)
        user.save()

        serializer = UserProfileSerializer(user)

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def login(request):
    errors = Error()
    params = request.data
    print(params)

    login = params.get('login')
    password = params.get('password')
    country_id = params.get("country_id")

    if request.method == 'POST':
        print("POST")

        if (login == None or password == None):
            errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(login=login, password=password)
            print("NOT ERROR EXIST")
        except UserProfile.DoesNotExist:
            errors.append(ErrorMessages.LOGIN_ERROR_401)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_401_UNAUTHORIZED)

        country = Countries.objects.get(id=country_id)
        user.country = country
        user.save()
        serializer = UserProfileSerializer(user)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_all_countries(request):
    countries = Countries.objects.all()

    serializer = CountriesSerializer(countries, many=True)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['GET'])
def get_all_types(request):
    errors = Error()
    params = request.data
    print(params)

    types = Types.objects.all()

    serializer = TypesSerializer(types, many=True)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

# @csrf_exempt
# @api_view(['GET'])
# def get_country(request, id):
#     country = Countries.objects.get(id=id)
#
#     data = {
#         JsonKey.Countries.ID: country.id,
#         JsonKey.Countries.TITLE: country.title,
#         JsonKey.Countries.PREFIX: country.prefix
#     }
#
#     print(data)
#
#     return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['PUT'])
def update_country(request, userprofile_id):
    errors = Error()
    params = request.data
    print(params)

    country_id = params.get(JsonKey.Countries.ID)

    if (country_id == None):
        errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)

    try:
        country = Countries.objects.get(id=country_id)
        print("NOT ERROR EXIST")
    except Countries.DoesNotExist:
        errors.append(ErrorMessages.COUNTRIES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)


    user = UserProfile.objects.get(id=userprofile_id)
    user.country = country
    user.save()

    serializer = UserProfileSerializer(user)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['GET'])
def show_histories(request, userprofile_id):
    errors = Error()

    user = UserProfile.objects.get(id = userprofile_id)
    histories = Histories.objects.filter(user = user)

    if len(histories) == 0:
        errors.append(ErrorMessages.HISTORIES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_200_OK)

    for item in histories:
        item.fact.type.title = Helpers.translate_language(user.country.prefix, item.fact.type.title)
        item.fact.description = Helpers.translate_language(user.country.prefix, item.fact.description)
    serializer = HistoriesSerializer(histories, many=True)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['DELETE'])
def delete_histories(request, userprofile_id, history_id):
    errors = Error()
    user = UserProfile.objects.get(id=userprofile_id)

    try:
        history = Histories.objects.get(user=user, id = history_id)
        print("NOT ERROR EXIST")
    except Histories.DoesNotExist:
        errors.append(ErrorMessages.HISTORY_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    history.delete()

    return HttpResponse(status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def get_random_fact(request, type):
    errors = Error()
    params = request.data
    print(params)

    userprofile_id = params.get(JsonKey.USERPROFILE_ID)

    headers = {
        "Content-Type": "application/json"
    }

    if (type == None or len(Types.objects.filter(en_title = type)) == 0):
        errors.append(ErrorMessages.GET_RANDOM_TYPES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    if (userprofile_id == None):
        errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    user = UserProfile.objects.get(id=userprofile_id)

    urlList = {
        'trivia': ApiUrl.RANDOM_TRIVIA,
        'year': ApiUrl.RANDOM_YEAR,
        'math': ApiUrl.RANDOM_MATH,
    }

    response = requests.get(headers=headers, url=urlList[type])
    print(response.text)
    obj = json.loads(response.text)

    type = Types.objects.get(en_title=obj["type"])
    number = obj["number"]
    description = obj["text"]
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fact = Fact.objects.create(type=type, number=number, description=description, date=date)
    fact.save()

    history = Histories.objects.create(user=user, fact=fact)
    history.save()

    history.fact.type.title = Helpers.translate_language(user.country.prefix, history.fact.type.title)
    history.fact.description = Helpers.translate_language(user.country.prefix, history.fact.description)

    serializer = FactsSerializer(fact)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['POST'])
def get_fact_by_type(request, type, number):
    errors = Error()
    params = request.data
    print(params)

    userprofile_id = params.get(JsonKey.USERPROFILE_ID)

    headers = {
        "Content-Type": "application/json"
    }

    if (type == None or len(Types.objects.filter(en_title=type)) == 0):
        errors.append(ErrorMessages.GET_RANDOM_TYPES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    user = UserProfile.objects.get(id=userprofile_id)

    url=ApiUrl.GENERATE_URL_BY_NUMBER_AND_TYPE.format(number, type)

    response = requests.get(headers=headers, url=url)
    print(response.text)
    obj = json.loads(response.text)

    type = Types.objects.get(en_title=obj["type"])
    number = obj["number"]
    description = obj["text"]
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fact = Fact.objects.create(type=type, number=number, description=description, date=date)
    fact.save()

    history = Histories.objects.create(user=user, fact=fact)
    history.save()

    history.fact.type.title = Helpers.translate_language(user.country.prefix, history.fact.type.title)
    history.fact.description = Helpers.translate_language(user.country.prefix, history.fact.description)

    serializer = FactsSerializer(fact)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)