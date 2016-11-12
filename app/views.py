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

from app import settings, forms
from cache import CacheSql
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
        context['form'] = forms.SurveyForm(
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
        context = {
            "courses": response.json(),
            "type": typ,
            "course": course,
            'path': settings.LOGO_IMAGE_STATIC
        }
        #  Cache().save(context['courses'])
        CacheSql().save(context['courses'])
        return {'context': context}


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
        if self.kwargs['save'].lower() == "true":
            data['username'] = request.user.username
            data_qs = urllib.urlencode(data)
            url = '{}/users/profile?{}'.format(settings.PALOMA_HOST, data_qs)
            response = requests.post(url, data_qs)
            if response.status_code != 200:
                return render(
                    request,
                    'app/courses.html',
                    {'error_message': 'Algo aconteceu errado: status code'}
                )
        filter = urllib.urlencode(data)
        url = '{}/courses?{}'.format(settings.PALOMA_HOST, filter)
        response = requests.get(url)
        if response.status_code != 200:
            return render(
                request,
                'app/courses.html',
                {'error_message': 'Algo aconteceu errado: status code: {}'.format(response.status_code)}
            )
        context = {
            'courses': response.json(),
            "type": self.kwargs['type'],
            "course": self.kwargs['course'],
            'path': settings.LOGO_IMAGE_STATIC
        }
        #  Cache().save(context['courses'])
        CacheSql().save(context['courses'])
        return render(request, 'app/courses.html', {'context': context})


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


class AvailableCoursesView(TemplateView):
    template_name = "app/available_courses.html"

    def get_context_data(self, **kwargs):
        url = '{}/types/courses'.format(settings.PALOMA_HOST)
        response = requests.get(url)
        if response.status_code != 200:
            return {
                'error_message': 'Algo aconteceu errado: status code: {}'
                .format(response.status_code)
            }
        context = {
            "types": response.json(),
            "path": settings.TYPES_IMAGE_STATIC,
            "photo_default": '{}default'.format(settings.TYPES_IMAGE_STATIC)
        }
        return {'context': context}

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = forms.UserFormLogin()
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
                {'form': forms.UserFormLogin(), 'alert_error': "Usuário ou senha incorretos"}
            )

        return render(request, 'app/index.html', {})


# TODO: Fazer request para o servidor guardar tais informações no banco de dados
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = forms.UserFormSignUp()
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
        form = forms.UpdatePasswordForm()
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
        form = forms.IndicateCourseForm(type, course)
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
        if os.path.exists(settings.USER_IMAGE_PATH_COMPLETE + username):
            photo = username
        context = {
            'photo': photo,
            'path': settings.USER_IMAGE_STATIC,
            'name': '{} {}'.format(user.first_name, user.last_name),
            'email': user.email,
            'username': user.username,
            'last_login': user.last_login,
            'date_joined': user.date_joined,
        }
        return render(request, 'app/profile.html', {'context': context})


class UploadImageView(View):
    def post(self, request, *args, **kwargs):
        data = {
           "username": "username",
        }
        data_qr = urllib.urlencode(data)
        url_req = "{}/users/profile?{}".format(settings.PALOMA_HOST, data_qr) 
        response = requests.post(url_req)
        path = settings.USER_IMAGE_PATH_COMPLETE
        file = request.FILES['image']
        name = request.user.username
        with open(default_storage.path(path + name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return redirect('app:profile')


class CourseDetailView(View):
    def fmt_list(self, ufmt, fmt, char):
        result = []
        if char == "Price":
            if ufmt["PriceReal"] != None:
                for value in ufmt["PriceReal"]:
                    result.append('R${},00'.format(value))
            if ufmt["PriceDolar"] != None:
                for value in ufmt["PriceDolar"]:
                    result.append('${},00'.format(value))
        else:
            for value in ufmt[char]:
                for dict in fmt[0][char]:
                    if dict.get(value) != None:
                        result.append(dict.get(value))
        return result

    def fmt_table(self, detail, char):
        result = {
            "name": {
                "label": "Name",
                "value": detail["Name"],
            },
            "url": {
                "label": "Endereço",
                "value": detail["Url"],
            },
            "based": {
                "label": "Baseado em",
                "value": self.fmt_list(detail, char, "Based"),
            },
            "platform": {
                "label": "Plataforma",
                "value": self.fmt_list(detail, char, "Platform"),
            },
            "extra": {
                "label": "Característica extras",
                "value": self.fmt_list(detail, char, "Extra"),
            },
            "dynamic": {
                "label": "Dinâmica do curso",
                "value": self.fmt_list(detail, char, "Dynamic"),
            },
            "price": {
                "label": "Preços",
                "value": self.fmt_list(detail, char, "Price"),
            }
        }
        return json.dumps(result)

    def get(self, request, *args, **kwargs):
        context = {
            "name": self.kwargs['name'],
            "type": self.kwargs["type"],
            "course": self.kwargs["course"],
        }
        detail = {}
        try:
            detail = CacheSql().get(context['name'])
        except: 
            url = '{}/course/detail?type={}&course={}&name={}'.format(settings.PALOMA_HOST, context['type'], context['course'], context['name'])
            response = requests.get(url)
            if response.status_code != 200:
                return {
                    'error_message': 'Algo aconteceu errado: status code: {}'
                    .format(response.status_code)
                }
            detail = response.json()
        url = '{}/courses/questions?type={}'.format(settings.PALOMA_HOST, context['type'])
        response = requests.get(url)
        if response.status_code != 200:
            return {
                'error_message': 'Algo aconteceu errado: status code: {}'
                .format(response.status_code)
            }
        list_char = response.json()

        formated_courses = self.fmt_table(detail, list_char)
        context["courses"] = formated_courses
        return JsonResponse(json.dumps({'context': context}), safe=False)
