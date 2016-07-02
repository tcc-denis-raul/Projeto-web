# -*- coding: utf-8 -*-
import json

from django.views.generic import TemplateView, View
from django.http import JsonResponse

# Create your views here.


class IndexView(TemplateView):
    template_name = 'app/index.html'


class SurveyView(TemplateView):
    template_name = 'app/survey.html'


class CoursesView(TemplateView):
    template_name = 'app/courses.html'

    # TODO: fazer request para api
    # endereco: courses/language/course
    # method: get
    # envia a typ e course
    # return: lista json com todos os cursos para a language e o curso (ex. language/ingles)
    def get_context_data(self, **kwargs):
        typ = self.kwargs['type']
        course = self.kwargs['course']
        print typ
        print course
        return_example = [
            {
                "preco-dolar": [0],
                "url": "https://www.duolingo.com/pt",
                "based": ["exemplo", "exercicio_interativo"],
                "name": "Duolingo",
                "extra": ["comunicacao_alunos"],
                "dinamica": ["curso_livre"],
                "preco_real": [0],
                "plataforma": ["android_online", "ios_online"],
                "descricao": "preecher"
            }
        ]
        return {'courses': return_example}


class TypesCoursesView(View):

    # TODO: fazer o request para a api
    # endereço: /types/courses
    # method: get
    # return: json
    def get(self, request, *args, **kwargs):
        types_courses = {'language': ['ingles']}
        return JsonResponse(json.dumps(types_courses), safe=False)
