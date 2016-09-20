# -*- coding: utf-8 -*-
import json
import requests
import urllib
import os

from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage

from app import settings
from .forms import SurveyForm, UserFormLogin, UserFormSignUp, UpdatePasswordForm, IndicateCourseForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'app/index.html'


class SurveyView(TemplateView):
    template_name = 'app/survey.html'

    def fmt_list(self, value):
        list = []
        for i in value:
            list.append((i.keys()[0], i.values()[0], ))
        return list

    def get_context_data(self, **kwargs):
        context = {
            'type': self.kwargs['type'],
            'save': self.kwargs['save'],
        }
        url = '{}/courses/questions?type={}'.format(settings.PALOMA_HOST, context['type'])
        response = requests.get(url)
        if response.status_code != 200:
            # TODO: Tratar todos os erros possiveis: 
            # ex.: 404 gerar pagina de 404 ...
            return {
                'error_message': 'Algo aconteceu errado: status code: {}'
                .format(response.status_code)
            }
        context['form'] = SurveyForm(
            self.fmt_list(response.json()[0]['Price']),
            self.fmt_list(response.json()[0]['Based']),
            self.fmt_list(response.json()[0]['Platform']),
            self.fmt_list(response.json()[0]['Dynamic']),
            self.fmt_list(response.json()[0]['Extra'])
        )
        return {'context': context}


class CoursesView(TemplateView):
    template_name = 'app/courses.html'

    def get_context_data(self, **kwargs):
        typ = self.kwargs['type']
        course = self.kwargs['course']
        url = '{}/courses?type={}&course={}'.format(settings.PALOMA_HOST, typ, course)

        response = requests.get(url)
        if response.status_code != 200:
            #TODO: Tratar todos os erros possiveis
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
        if request.GET['save'].lower() == "true":
            # TODO: Send data to api, api store the data
            print data
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
        return render(request, 'app/form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        userName = request.POST['UserName']
        password = request.POST['Password']
        user = authenticate(username=userName, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                return render(
                    request,
                    'app/form.html',
                    {
                        'form': UserFormLogin(),
                        'alert_error': "Conta desabilitada. Entre em contato com o Administrador"
                    }
                )
        else:
            return render(
                request,
                'app/form.html',
                {'form': UserFormLogin(), 'alert_error': "Usuário ou senha incorretos"}
            )

        return render(request, 'app/index.html', {})


# TODO: Fazer request para o servidor guardar tais informações no banco de dados
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = UserFormSignUp()
        return render(request, 'app/form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        userName = request.POST['UserName']
        email = request.POST['Email']
        firstName = request.POST['FirstName']
        lastName = request.POST['LastName']
        password = request.POST['Password']
        confirm = request.POST['Confirm']
        if confirm != password:
            return render(
                request,
                "app/form.html",
                {'alert_error': 'Senhas não coicidem', 'form': UserFormSignUp()}
            )
        user = User.objects.create_user(userName, email, password)
        user.first_name = firstName
        user.last_name = lastName
        user.save()
        return redirect('app:login')


# TODO: fazer request para api salvar o ultimo acesso
class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'app/index.html', {})


class UpdatePasswordView(View):
    def get(self, request, *args, **kwargs):
        form = UpdatePasswordForm()
        return render(request, 'app/form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        username = request.user.username
        newPasswd = request.POST['NewPasswd']
        confirm = request.POST['Confirm']
        if confirm != newPasswd:
            return render(
                request,
                "app/form.html",
                {'alert_error': 'Senhas não coicidem', 'form': UpdatePasswordForm()}
            )
        u = User.objects.get(username=username)
        u.set_password(newPasswd)
        u.save()
        return render(request, 'app/index.html', {})


class IndicateCourseView(View):
    def get(self, request, *args, **kwargs):
        type = [('Language', 'Idiomas', )]
        course = [('Ingles', 'Ingles', )]
        form = IndicateCourseForm(type, course)
        return render(request, 'app/form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        data = {
           "type": request.POST['Type'],
            "course": request.POST['Course'],
            "name": request.POST['Name'],
            "url": request.POST['Url']
        }
        data_qr = urllib.urlencode(data)
        url_req = "{}/indicate/course?{}".format(settings.PALOMA_HOST, data_qr) 
        response = requests.post(url_req)
        if response.status_code != 200:
            return render(
                request,
                "app/index.html",
                {'alert_error': 'Curso já cadastrado ou indicado'}
            )
        return render(request, 'app/index.html', {})


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        username = request.user.username
        user = User.objects.get(username=username)
        photo = 'default'
        if os.path.exists(settings.IMAGE_PATH + username):
            photo = username
        context = {
            'photo': photo,
            'path': settings.IMAGE_PATH_STATIC,
            'name': '{} {}'.format(user.first_name, user.last_name),
            'email': user.email,
            'username': user.username,
            'last_login': user.last_login,
            'date_joined': user.date_joined,
        }
        return render(request, 'app/profile.html', {'context': context})


class UploadImageView(View):
    def post(self, request, *args, **kwargs):
        path = settings.IMAGE_PATH
        file = request.FILES['image']
        name = request.user.username
        with open(default_storage.path(path + name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return redirect('app:profile')
