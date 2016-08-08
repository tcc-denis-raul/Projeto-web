# -*- coding: utf-8 -*-
import json
import requests

from django.views.generic import TemplateView, View
from django.http import JsonResponse

from app import settings
from .forms import SurveyForm
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
        return {'form': form}


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
