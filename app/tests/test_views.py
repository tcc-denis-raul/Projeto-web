# -*- coding: utf-8 -*-
import httpretty
import requests
import urllib
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User

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
        self.assertRedirects(
            response,
            expected_url=reverse('app:error', kwargs={'status': 500}),
            status_code=302,
            target_status_code=200
        )


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
        self.assertRedirects(
            response,
            expected_url=reverse('app:error', kwargs={'status': 500}),
            status_code=302,
            target_status_code=200
        )


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
        self.assertRedirects(
            response,
            expected_url=reverse('app:error', kwargs={'status': 400}),
            status_code=302,
            target_status_code=200
        )

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
        self.assertRedirects(
            response,
            expected_url=reverse('app:error', kwargs={'status': 500}),
            status_code=302,
            target_status_code=200
        )


class TestTypesCoursesView(TestCase):

    @httpretty.activate
    def test_get_types_courses(self):
        data = '[{"Language": ["ingles"]}]'
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/types/courses",
            body=data
        )
        response = self.client.get(reverse('app:types_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json()), data)

    @httpretty.activate
    def test_get_types_courses_status_not_found(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/types/courses",
            status=404
        )
        response = self.client.get(reverse('app:types_courses'))
        self.assertRedirects(
            response,
            expected_url=reverse('app:error', kwargs={'status': 404}),
            status_code=302,
            target_status_code=200
        )


class TestLoginView(TestCase):

    def test_get_user_form_login(self):
        response = self.client.get(reverse('app:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/form.html')
        self.assertContains(response, 'Usuário')
        self.assertContains(response, 'Senha')

    def test_post_user_login_not_found_user(self):
        response = self.client.post(
            reverse('app:login'),
            {'UserName': 'test', 'Password': 'test'}
        )
        self.assertRedirects(
            response,
            expected_url=reverse('app:login'),
            status_code=302,
            target_status_code=200
        )

    def test_post_user_login(self):
        user = User.objects.create_user('test', 'test', 'test')
        user.first_name = 'test'
        user.last_name = 'test'
        user.save()
        response = self.client.post(
            reverse('app:login'),
            {'UserName': 'test', 'Password': 'test'}
        )
        self.assertRedirects(
            response,
            expected_url=reverse('app:index'),
            status_code=302,
            target_status_code=200
        )


class TestSignUpView(TestCase):

    def test_get_sign_up_view(self):
        response = self.client.get(reverse('app:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/form.html')
        self.assertContains(response, 'Usuário')
        self.assertContains(response, 'Primeiro nome')
        self.assertContains(response, 'Último nome')
        self.assertContains(response, 'Senha')
        self.assertContains(response, 'Email')

    def test_post_sign_up_view(self):
        response = self.client.post(
            reverse('app:signup'),
            {
                'UserName': 'test',
                'Email': 'test',
                'FirstName': 'test',
                'LastName': 'test',
                'Password': 'test',
                'Confirm': 'test'
            }
        )
        self.assertRedirects(
            response,
            expected_url=reverse('app:login'),
            status_code=302,
            target_status_code=200
        )
        user = User.objects.get()
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test')
        user.delete()

    def test_post_wrong_password_sign_up(self):
        response = self.client.post(
            reverse('app:signup'),
            {
                'UserName': 'test',
                'Email': 'test',
                'FirstName': 'test',
                'LastName': 'test',
                'Password': 'test',
                'Confirm': 'wrong'
            }
        )
        self.assertRedirects(
            response,
            expected_url=reverse('app:signup'),
            status_code=302,
            target_status_code=200
        )


class TestLogoutView(TestCase):

    def test_get_logout(self):
        response = self.client.get(reverse('app:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/form.html')
        self.assertContains(response, 'Desconectar')


    def test_post_logout(self):
        response = self.client.post(reverse('app:logout'))
        self.assertRedirects(
            response,
            expected_url=reverse('app:index'),
            status_code=302,
            target_status_code=200
        )


class TestUpdatePasswordView(TestCase):

    def test_get_update_password(self):
        response = self.client.get(reverse('app:update_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/form.html')
        self.assertContains(response, 'Nova senha')
        self.assertContains(response, 'Confirmar senha')

    def test_post_update_password(self):
        user = User.objects.create_user('test', 'test', 'test')
        user.save()
        old_passwd = User.objects.get(username='test').password
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('app:update_password'),
            {'NewPasswd': 'test2', 'Confirm': 'test2'}
        )
        self.assertRedirects(
            response,
            expected_url=reverse('app:index'),
            status_code=302,
            target_status_code=200
        )
        user = User.objects.get(username='test')
        self.assertNotEqual(old_passwd, user.password)

    def test_post_update_password_wrong(self):
        user = User.objects.create_user('test', 'test', 'test')
        user.save()
        old_passwd = User.objects.get(username='test').password
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('app:update_password'),
            {'NewPasswd': 'test2', 'Confirm': 'test'}
        )
        self.assertRedirects(response, expected_url=reverse('app:update_password'), status_code=302, target_status_code=200)


class TestUpdateUserView(TestCase):

    def test_get_udpate_user_view(self):
        response = self.client.get(reverse('app:update_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/form.html')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Primeiro nome')
        self.assertContains(response, 'Último nome')

    def test_post_udpate_user_view(self):
        user = User.objects.create_user('test', 'test', 'test')
        user.first_name = 'first'
        user.last_name = 'last'
        user.save()
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('app:update_user'),
            {
                'Email': 'email',
                'FirstName': 'first2',
                'LastName': 'last2'
            }
        )
        self.assertRedirects(
            response,
            expected_url=reverse('app:profile'),
            status_code=302,
            target_status_code=200
        )
        user = User.objects.get(username='test')
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'email')
        self.assertEqual(user.first_name, 'first2')
        self.assertEqual(user.last_name, 'last2')


class TestIndicateCourseView(TestCase):

    def test_get_forms_indicate(self):
        response = self.client.get(reverse('app:indicate_course'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/form.html')
        self.assertContains(response, 'Tipo do curso')
        self.assertContains(response, 'Idioma')
        self.assertContains(response, 'Nome do curso')
        self.assertContains(response, 'Endereco do curso')

    @httpretty.activate
    def test_post_indicate_course(self):
        data = {
            "type": "language",
            "course": "ingles",
            "name": "test",
            "url": "test"
        }
        data_qr = urllib.urlencode(data)
        httpretty.register_uri(
            httpretty.POST,
            "http://localhost:5000/indicate/course?{}".format(data_qr)
        )
        response = self.client.post(
            reverse('app:indicate_course'),
            {
                "Type": 'language',
                "Course": "ingles",
                "Name": "test",
                "Url": "test"
            }
        )
        self.assertRedirects(
            response,
            expected_url=reverse('app:index'),
            status_code=302,
            target_status_code=200
        )

    @httpretty.activate
    def test_post_indicate_course_status_not_200(self):
        data = {
            "type": "language",
            "course": "ingles",
            "name": "test",
            "url": "test"
        }
        data_qr = urllib.urlencode(data)
        httpretty.register_uri(
            httpretty.POST,
            "http://localhost:5000/indicate/course?{}".format(data_qr),
            status=500
        )
        response = self.client.post(
            reverse('app:indicate_course'),
            {
                "Type": 'language',
                "Course": "ingles",
                "Name": "test",
                "Url": "test"
            }
        )
        self.assertRedirects(
            response,
            expected_url=reverse('app:index'),
            status_code=302,
            target_status_code=200
        )

class TestProfielView(TestCase):

    def test_get_profile(self):
        user = User.objects.create_user('test', 'test', 'test')
        user.first_name = 'first'
        user.last_name = 'last'
        user.save()
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('app:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/profile.html')
        self.assertContains(response, user.username)
        self.assertContains(response, 'default')
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.email)


class TestAvailableCoursesView(TestCase):

    @httpretty.activate
    def test_get_available_courses(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/types/courses",
            body='[{"Language":["ingles"]}]'
        )
        response = self.client.get(reverse('app:available_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/available_courses.html')

    @httpretty.activate
    def test_get_available_courses_wrong(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:5000/types/courses",
            status=404
        )
        response = self.client.get(reverse('app:available_courses'))
        self.assertRedirects(
            response,
            expected_url=reverse('app:error', kwargs={'status': 404}),
            status_code=302,
            target_status_code=200
        )
