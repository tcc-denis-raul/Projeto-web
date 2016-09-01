from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^survey/(?P<type>[\w+]+)/$', views.SurveyView.as_view(), name='survey'),
    url(r'^types/courses/$', views.TypesCoursesView.as_view(), name='types_courses'),
    url(r'^courses/(?P<type>[\w+]+)/(?P<course>[\w+]+)/$', views.CoursesView.as_view(), name='courses'),
    url(r'^survey/(?P<type>[\w+]+)/(?P<course>[\w+]+)/result/$', views.ResultSurveyView.as_view(), name='result_survey'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^logout/$', views.LogOutView.as_view(), name='logout'),
    url(r'^password/update/$', views.UpdatePasswordView.as_view(), name='update_password'),
    url(r'^indicate/course/$', views.IndicateCourseView.as_view(),
        name='indicate_course'),
]
