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
from .constant.API import API
from .constant.ErrorMessages import ErrorMessages
from .constant.JsonKey import JsonKey
from .models import UserProfile, Error, Language, Histories, Cities, Weather


@csrf_exempt
@api_view(['POST'])
def registration(request):
    errors = Error()
    params = request.data
    print(params)

    login = params.get('login')
    password = params.get('password')
    language_id = params.get('language_id')

    if request.method == 'POST':
        print("POST")

        if (login == None or password == None or language_id == None):
            errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)

        language = Language.objects.get(id=language_id)

        try:
            UserProfile.objects.get(login=login, password=password)
            print("NOT ERROR EXIST")
            # Если есть зареганый аккаунт, то сработает этот сценарий
            errors.append(ErrorMessages.REGISTRATION_ERROR_400)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            pass

        user = UserProfile.objects.create(login=login, password=password, language=language)
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
    language_id = params.get("language_id")

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

        language = Language.objects.get(id=language_id)
        user.language = language
        user.save()
        serializer = UserProfileSerializer(user)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_all_languages(request):
    languages = Language.objects.all()

    serializer = LanguageSerializer(languages, many=True)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
@api_view(['GET'])
def get_all_cities(request):
    params = request.data

    types = Cities.objects.all()

    serializer = CitiesSerializer(types, many=True)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['PUT'])
def update_language(request, userprofile_id):
    errors = Error()
    params = request.data
    print(params)

    language_id = params.get(JsonKey.Language.ID)

    if (language_id == None):
        errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)

    try:
        language = Language.objects.get(id=language_id)
        print("NOT ERROR EXIST")
    except Language.DoesNotExist:
        errors.append(ErrorMessages.COUNTRIES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)


    user = UserProfile.objects.get(id=userprofile_id)
    user.language = language
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
def get_weather(request, city_name):
    errors = Error()
    params = request.data
    print(params)

    userprofile_id = params.get(JsonKey.USERPROFILE_ID)

    headers = {
        "Content-Type": "application/json"
    }

    city = Cities.objects.filter(title=city_name)
    if (city == None or len(city) == 0):
        errors.append(ErrorMessages.CITIES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    if (userprofile_id == None):
        errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    city = city[0]
    user = UserProfile.objects.get(id=userprofile_id)

    URL = API.GENERATE_URL.format(city.title, city.country_code, user.language.prefix, API.API_KEY)

    response = requests.get(headers=headers, url=URL)
    print(response.text)
    obj = json.loads(response.text)

    obj = obj['data'][0]
    temp = obj['temp']

    weather_response = obj['weather']
    description = weather_response['description']
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    weather = Weather.objects.create(city=city, temp=temp, description=description, date=date)
    weather.save()

    history = Histories.objects.create(user=user, weather=weather)
    history.save()

    serializer = HistoriesSerializer(history)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)