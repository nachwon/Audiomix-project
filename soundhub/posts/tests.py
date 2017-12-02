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

    # 테스트 유저 생성
    @staticmethod
    def create_user(email='testuser@test.co.kr', nickname='testuser'):
        return User.objects.create_user(
            email=email,
            nickname=nickname,
            password='testpassword'
        )

    # 테스트 포스트 생성
    def create_post(self):
        # 유저 생성
        user = self.create_user()
        # 포스트 생성
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
        return response

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
        # 포스트 생성
        response = self.create_post()

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
        # self.assertTrue(filecmp.cmp(track_dir, post.author_track.file.name))


class PostDetailAPIViewTest(APILiveServerTestCase):
    API_VIEW_URL = '/post/'

    # 테스트 유저 생성
    @staticmethod
    def create_user(email='testuser@test.co.kr', nickname='testuser'):
        return User.objects.create_user(
            email=email,
            nickname=nickname,
            password='testpassword'
        )

    # 테스트 포스트 생성
    def create_post(self):
        # 유저 생성
        user = self.create_user()
        # 포스트 생성
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
        return response

    # 포스트 조회 테스트
    def test_post_retrieve(self):
        # 포스트 생성
        self.create_post()

        # 비교대상 포스트
        post = Post.objects.get(pk=1)

        # 생성한 포스트 가져오기
        response = self.client.get('http://testserver/post/1/')

        # 데이터베이스에서 꺼내온 포스트와 /post/1/의 응답으로 받은 포스트를 비교
        self.assertEqual(response.data['id'], post.pk)
        self.assertEqual(response.data['title'], post.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author_track'], post.author_track)

    # 포스트 수정 테스트
    def test_post_update(self):
        # 포스트 생성
        self.create_post()

        # /post/3/으로 PATCH 요청을 보냄
        factory = APIRequestFactory()
        data = {
            'title': 'updated_title',
        }
        request = factory.patch('/post/2/', data)
        view = PostDetail.as_view()
        response = view(request, pk=2)

        # 인증 정보가 없는 경우 포스트 수정 불가인지 확인
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 작성자가 아닌 경우 포스트 수정 불가능한지 확인
        self.create_user('testuser2@test.co.kr', 'testuser2')
        user = User.objects.get(email='testuser2@test.co.kr')
        user.refresh_from_db()
        force_authenticate(request, user=user)
        response = view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 작성자인 경우 포스트 수정 성공 확인
        user = User.objects.get(email='testuser@test.co.kr')
        force_authenticate(request, user=user)
        response = view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'updated_title')

