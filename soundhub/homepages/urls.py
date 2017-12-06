from django.conf.urls import url

from .views import HomePageView, GenreHomePageView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^genre/(?P<genre>[a-zA-Z]+)/$', GenreHomePageView.as_view(), name='genre-home'),
]