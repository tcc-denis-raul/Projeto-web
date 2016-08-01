from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^survey/(?P<type>[\w+]+)/$', views.SurveyView.as_view(), name='survey'),
    url(r'^types/courses/$', views.TypesCoursesView.as_view(), name='types_courses'),
    url(r'^courses/(?P<type>[\w+]+)/(?P<course>[\w+]+)/$', views.CoursesView.as_view(), name='courses')

]
