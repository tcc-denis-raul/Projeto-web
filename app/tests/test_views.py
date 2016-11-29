# -*- coding: utf-8 -*-
import httpretty
import requests
from django.test import TestCase
from django.core.urlresolvers import reverse

class TestErrorView(TestCase):

    def test_template_used(self):
        response = self.client.get(reverse('app:error', kwargs={'status': 404}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/404.html')
        self.assertContains(response, '404')

    def test_template_wrong_status_code(self):
        response = self.client.get(reverse('app:error', kwargs={'status': 500}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/404.html')
        self.assertNotContains(response, '404')

class TestIndexView(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/index.html')



class TestSurveyView(TestCase):

    @httpretty.activate
    def test_get_questions_status_ok(self):
        data = '[{"Based":[{"texto":"Textos"},{"video_aula":"Video aulas"},{"exemplo":"Examplos"},{"exercicio_interativo":"Exercicios interativos"}],"Price":[{"gratis":"Grátis"},{"ate30":"Até 30 reais"},{"31a60":"De 31 a 60 reais"},{"61a100":"De 61 a 100 reais"},{"101a150":"De 101 a 150 reais"},{"151mais":"Mais de 151 reais"}],"Dynamic":[{"curso_livre":"Curso Livre"},{"tempo_definido":"Tempo de Curso Definido"},{"inicio_definido":"Data de Início Definida"}],"Platform":[{"android_offline":"Android - Offline"},{"android_online":"Android - Online"},{"ios_offline":"IOS - Offline"},{"ios_online":"IOS - Online"},{"desktop_offline":"Desktop - Offline"},{"desktop_online":"Desktop - Online"}],"Extra":[{"selecao_nivel":"Seleção de Nível de conhecimento"},{"professor":"Professor Disponível"},{"comunicacao_alunos":"Comunicação entre alunos"}]}]'
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/courses/questions?type=language",
            body=data,
            content_type="application/json"
        )
        response = self.client.get(reverse('app:survey', kwargs={'type': 'language', 'save': 'true'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/survey.html')
        self.assertContains(response, 'Video aulas')

    @httpretty.activate
    def test_get_questions_status_not_found(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/courses/questions?type=language",
            status=500
        )
        response = self.client.get(reverse('app:survey', kwargs={'type': 'language', 'save': 'false'}))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'app/survey.html')
