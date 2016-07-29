# -*- coding: utf-8 -*-
import json
import requests

from django.views.generic import TemplateView, View
from django.http import JsonResponse

from app import settings
# Create your views here.


class IndexView(TemplateView):
    template_name = 'app/index.html'


class SurveyView(TemplateView):
    template_name = 'app/survey.html'


class CoursesView(TemplateView):
    template_name = 'app/courses.html'

    def get_context_data(self, **kwargs):
        typ = self.kwargs['type']
        course = self.kwargs['course']
        url = '{}/courses?type={}&course={}'.format(settings.PALOMA_HOST, typ, course)
        response = requests.get(url)
        if response.status_code != 200:
            return {
                'error_message': 'Algo aconteceu errado: status code: {}'.format(response.status_code)
            }

        return {'courses': response.json()}


class TypesCoursesView(View):

    def get(self, request, *args, **kwargs):
        url = '{}/types/courses'.format(settings.PALOMA_HOST)
        response = requests.get(url)
        if response.status_code != 200:
            return {
                'error_message': 'Algo aconteceu errado: status code: {}'.format(response.status_code)
            }
        return JsonResponse(json.dumps(response.json()), safe=False)
