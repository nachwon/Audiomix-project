from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from rest_framework.test import APILiveServerTestCase

from posts.views import PostList

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    API_VIEW_URL = '/post/'
    API_VIEW_URL_NAME = 'post:list'
    VIEW_CLASS = PostList

    @staticmethod
    def create_user(username='testuser@test.co.kr'):
        return User.objects.create_user(username=username, nickname='testuser')

    # PostList URL로 접속했을 때 PostList 뷰를 사용하고 있는지 테스트
    def test_post_list_url_resolve(self):
        resolve_match = resolve(self.API_VIEW_URL)
        self.assertEqual(resolve_match.view_name, self.API_VIEW_URL_NAME)
        self.assertEqual(resolve_match.func.view_class, self.VIEW_CLASS)
