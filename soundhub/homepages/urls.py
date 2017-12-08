from django.conf.urls import url

from .views import HomePageView, GenreHomePageView, InstrumentHomePageView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^genre/(?P<genre>[a-zA-Z]+)/$', GenreHomePageView.as_view(), name='genre-home'),
    url(r'^instrument/(?P<instrument>[a-zA-Z]+)/$', InstrumentHomePageView.as_view(), name='inst-home'),
]
