# -*- coding: utf-8 -*-
import httpretty
import requests
import urllib
from django.test import TestCase
from django.core.urlresolvers import reverse

COURSES = '[{"ID":"5838544d7c298c4be7274a8d","Name":"Duolingo","Based":["exemplo","exercicio_interativo"],"PriceReal":[0],"PriceDolar":[0],"Dynamic":["curso_livre"],"Platform":["android_online","ios_online"],"Url":"https://www.duolingo.com/pt","Extra":["comunicacao_alunos"],"Description":"preecher","Rate":0.75,"Count":4}]'



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


class TestCoursesView(TestCase):

    @httpretty.activate
    def test_courses_view_status_ok(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/courses?type=language&course=ingles",
            body=COURSES,
            content_type="application/json"
        )
        response = self.client.get(reverse('app:courses', kwargs={'type': 'language', 'course': 'ingles'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/courses.html')
        self.assertContains(response, 'Duolingo')

    @httpretty.activate
    def test_courses_views_status_not_found(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/courses?type=language&course=ingles",
            status=500
        )
        response = self.client.get(reverse('app:courses', kwargs={'type': 'language', 'course': 'ingles'}))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'app/courses.html')


class TestResultView(TestCase):
    def mock_courses(self, status):
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/courses?type=language&course=ingles",
            body=COURSES,
            status=status
        )

    def mock_profile(self, status):
        data = {
            "type": 'language',
            "course": 'ingles',
            "based": 'based',
            "extra": 'extra',
            "price": 'price',
            "dynamic": 'dynamic',
            "platform": 'platform',
            "length": 5,
            "username": 'username'
        }
        httpretty.register_uri(
            httpretty.POST,
            "http://localhost:5000/users/profile?{}".format(urllib.urlencode(data)),
            status=status
        )

    @httpretty.activate
    def test_result_view_with_courses(self):
        self.mock_courses(200)
        response = self.client.post(
            reverse(
                'app:result_survey',
                kwargs={
                    'type': 'language',
                    'course': 'ingles',
                    'save': "false"
                }
            ),
            {'Based': 'based', 'Extra': 'extra', 'Price': 'price', 'Dynamic': 'dynamic', 'Platform': 'platform'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/courses.html')
        self.assertContains(response, 'Duolingo')

    @httpretty.activate
    def test_result_view_saving_profile(self):
        self.mock_courses(200)
        self.mock_profile(200)
        response = self.client.post(
            reverse(
                'app:result_survey',
                kwargs={
                    'type': 'language',
                    'course': 'ingles',
                    'save': "true"
                }
            ),
            {'Based': 'based', 'Extra': 'extra', 'Price': 'price', 'Dynamic': 'dynamic', 'Platform': 'platform', 'username': 'username'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/courses.html')

    @httpretty.activate
    def test_result_view_saving_profile_with_status_not_found(self):
        self.mock_courses(200)
        self.mock_profile(400)
        response = self.client.post(
            reverse(
                'app:result_survey',
                kwargs={
                    'type': 'language',
                    'course': 'ingles',
                    'save': "true"
                }
            ),
            {'Based': 'based', 'Extra': 'extra', 'Price': 'price', 'Dynamic': 'dynamic', 'Platform': 'platform', 'username': 'username'}
        )
        self.assertEqual(response.status_code, 302)

    @httpretty.activate
    def test_result_view_with_status_not_found(self):
        self.mock_courses(500)
        response = self.client.post(
            reverse(
                'app:result_survey',
                kwargs={
                    'type': 'language',
                    'course': 'ingles',
                    'save': "false"
                }
            ),
            {'Based': 'based', 'Extra': 'extra', 'Price': 'price', 'Dynamic': 'dynamic', 'Platform': 'platform'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'app/courses.html')
