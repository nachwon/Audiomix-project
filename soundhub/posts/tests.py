from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework.test import APILiveServerTestCase

from posts.views import PostList

User = get_user_model()


class PostListAPIViewTest(APILiveServerTestCase):
    API_VIEW_URL = '/post/'
    API_VIEW_URL_NAME = 'post:list'
    VIEW_CLASS = PostList

    # /post/로 접속했을 때 PostList 뷰를 사용하고 있는지 테스트
    def test_post_list_url_resolve(self):
        resolve_match = resolve(self.API_VIEW_URL)
        self.assertEqual(resolve_match.view_name, self.API_VIEW_URL_NAME)
        self.assertEqual(resolve_match.func.view_class, self.VIEW_CLASS)

    # post:list 을 호출했을 때 /post/ url으로 연결되는지 테스트
    def test_post_list_url_name_reverse(self):
        url = reverse(self.API_VIEW_URL_NAME)
        self.assertEqual(url, self.API_VIEW_URL)

