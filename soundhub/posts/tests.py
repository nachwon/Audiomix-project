import filecmp
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIRequestFactory, force_authenticate, RequestsClient

from posts.models import Post
from posts.views import PostList, PostDetail

User = get_user_model()


class PostListAPIViewTest(APILiveServerTestCase):
    API_VIEW_URL = '/post/'
    API_VIEW_URL_NAME = 'post:list'
    VIEW_CLASS = PostList

    @staticmethod
    def create_user(email='testuser@test.co.kr'):
        return User.objects.create_user(
            email=email,
            nickname='testuser',
            password='testpassword'
        )

    # /post/로 접속했을 때 PostList 뷰를 사용하고 있는지 테스트
    def test_post_list_url_resolve(self):
        resolve_match = resolve(self.API_VIEW_URL)
        self.assertEqual(resolve_match.view_name, self.API_VIEW_URL_NAME)
        self.assertEqual(resolve_match.func.view_class, self.VIEW_CLASS)

    # post:list 을 호출했을 때 /post/ url으로 연결되는지 테스트
    def test_post_list_url_name_reverse(self):
        url = reverse(self.API_VIEW_URL_NAME)
        self.assertEqual(url, self.API_VIEW_URL)

    # Post Create 테스트
    def test_post_create(self):
        user = self.create_user()
        factory = APIRequestFactory()
        track_dir = os.path.join(settings.MEDIA_ROOT, 'author_tracks/The_Shortest_Straw_-_Guitar.mp3')
        with open(track_dir, 'rb') as author_track:
            data = {
                'title': 'test_title',
                'author_track': author_track,
            }
            request = factory.post(self.API_VIEW_URL, data)
        force_authenticate(request, user=user)

        view = PostList.as_view()
        response = view(request)

        test_user = User.objects.first()
        post = Post.objects.get(pk=response.data['id'])

        # 제목 테스트
        self.assertEqual(response.data['title'], 'test_title')
        # 작성자 테스트
        self.assertEqual(response.data['author']['id'], test_user.pk)
        # 상태 코드 테스트
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 생성된 포스트 갯수 테스트
        self.assertEqual(Post.objects.count(), 1)
        # 파일 일치 테스트
        # self.assertTrue(filecmp.cmp(track_dir, post.author_track.file))
