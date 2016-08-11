# -*- coding: utf-8 -*-
import json
import requests
import urllib

from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render

from app import settings
from .forms import SurveyForm
from .forms import UserFormLogin
from .forms import UserFormSignUp
# Create your views here.


class IndexView(TemplateView):
    template_name = 'app/index.html'


class SurveyView(TemplateView):
    template_name = 'app/survey.html'

    def gera_list(self, value):
        list = []
        for i in value:
            list.append((i.keys()[0], i.values()[0], ))
        return list

    def get_context_data(self, **kwargs):
        typ = self.kwargs['type']
        url = '{}/courses/questions?type={}'.format(settings.PALOMA_HOST, typ)
        response = requests.get(url)
        if response.status_code != 200:
            return {
                'error_message': 'Algo aconteceu errado: status code: {}'
                .format(response.status_code)
            }

        form = SurveyForm(
            self.gera_list(response.json()[0]['Price']),
            self.gera_list(response.json()[0]['Based']),
            self.gera_list(response.json()[0]['Platform']),
            self.gera_list(response.json()[0]['Dynamic']),
            self.gera_list(response.json()[0]['Extra'])
        )
        return {'form': form, 'type': typ}


class CoursesView(TemplateView):
    template_name = 'app/courses.html'

    def get_context_data(self, **kwargs):
        typ = self.kwargs['type']
        course = self.kwargs['course']
        url = '{}/courses?type={}&course={}'.format(settings.PALOMA_HOST, typ, course)

        response = requests.get(url)
        if response.status_code != 200:
            return {
                'error_message': 'Algo aconteceu errado: status code: {}'
                .format(response.status_code)
            }

        return {'courses': response.json()}


class ResultSurveyView(View):
    def post(self, request, *args, **kwargs):
        data = {
            "type": self.kwargs['type'],
            "course": self.kwargs['course'],
            "based": request.POST['Based'],
            "extra": request.POST['Extra'],
            "price": request.POST['Price'],
            "dynamic": request.POST['Dynamic'],
            "platform": request.POST['Platform'],
            "length": 5
        }
        filter = urllib.urlencode(data)
        url = '{}/courses?{}'.format(settings.PALOMA_HOST, filter)
        response = requests.get(url)
        if response.status_code != 200:
            return render(
                request,
                'app/courses.html',
                {'error_message': 'Algo aconteceu errado: status code: {}'.format(response.status_code)}
            )
        return render(request, 'app/courses.html', {'courses': response.json()})


class TypesCoursesView(View):

    def get(self, request, *args, **kwargs):
        url = '{}/types/courses'.format(settings.PALOMA_HOST)
        response = requests.get(url)
        if response.status_code != 200:
            return {
                'error_message': 'Algo aconteceu errado: status code: {}'
                .format(response.status_code)
            }
        return JsonResponse(json.dumps(response.json()), safe=False)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserFormLogin()
        return render(request, 'app/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        email = request.POST['Email']
        password = request.POST['Password']
        user = authenticate(username=email, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

        return render(request, 'app/index.html', {})


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = UserFormSignUp()
        return render(request, 'app/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        email = request.POST['Email']
        name = request.POST['Name']
        password = request.POST['Password']
        confirm = request.POST['Confirm']
        if confirm != password:
            return render(
                request,
                "app/login.html",
                {'error_message': 'Senhas não coicidem'}
            )
        user = User.objects.create_user(name, email, password)
        user.save()
        return render(request, 'app/login.html', {})

class LogOutView(View):
    def get(self, requests, *args, **kwargs):
        logout(requests)
        return render(requests, 'app/index.html', {})
