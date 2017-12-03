import filecmp
import os
from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIRequestFactory, force_authenticate

from posts.models import Post
from posts.views import PostList, PostDetail

User = get_user_model()


# 포스트 리스트 API 테스트 - 포스트 생성, 리스트 조회
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
    def create_post(self, user):
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
        user = self.create_user()
        response = self.create_post(user=user)

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

    # 포스트 리스트 조회 테스트
    def test_post_list_retrieve(self):
        # 랜덤 갯수의 포스트 생성
        num = randint(0, 10)
        user = self.create_user()
        for i in range(num):
            self.create_post(user=user)

        # /post/ 에 GET 요청
        response = self.client.get(self.API_VIEW_URL)

        # 결과 테스트
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), num)


# 포스트 디테일 API 테스트 - 포스트 디테일 조회, 수정, 삭제
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
        pk = self.create_post().data['id']

        # 비교대상 포스트
        post = Post.objects.get(pk=pk)

        # 생성한 포스트 가져오기 - /post/pk/ 로 GET 요청
        response = self.client.get(f'http://testserver/post/{pk}/')

        # 데이터베이스에서 꺼내온 포스트와 /post/pk/의 응답으로 받은 포스트를 비교
        self.assertEqual(response.data['id'], post.pk)
        self.assertEqual(response.data['title'], post.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author_track'], post.author_track)

    # 포스트 수정 테스트
    def test_post_update(self):
        # 포스트 생성
        pk = self.create_post().data['id']

        # /post/pk/으로 PATCH 요청을 보냄
        factory = APIRequestFactory()
        data = {
            'title': 'updated_title',
        }
        request = factory.patch(f'/post/{pk}/', data)
        view = PostDetail.as_view()
        response = view(request, pk=pk)

        # 인증 정보가 없는 경우 포스트 수정 불가인지 확인
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 작성자가 아닌 경우 포스트 수정 불가능한지 확인
        user = self.create_user('testuser2@test.co.kr', 'testuser2')
        force_authenticate(request, user=user)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 작성자인 경우 포스트 수정 성공 확인
        user = User.objects.get(email='testuser@test.co.kr')
        force_authenticate(request, user=user)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'updated_title')

    # 포스트 삭제 테스트
    def test_post_destroy(self):
        # 포스트 생성
        pk = self.create_post().data['id']

        # /post/pk/으로 DELETE 요청을 보냄
        factory = APIRequestFactory()
        request = factory.delete(f'/post/{pk}/')
        view = PostDetail.as_view()
        response = view(request, pk=pk)

        # 인증 데이터가 없을 경우 포스트 삭제 불가 테스트
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 작성자가 아닌 경우 포스트 삭제 불가능한지 테스트
        user = self.create_user('testuser2@test.co.kr', 'testuser2')
        force_authenticate(request, user=user)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 작성자인 경우 삭제 가능
        user = User.objects.get(email='testuser@test.co.kr')
        force_authenticate(request, user=user)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 포스트가 삭제되었는지 확인
        request = factory.get(f'/post/{pk}/')
        view = PostDetail.as_view()
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentListAPIViewTest(APILiveServerTestCase):
    # 테스트 유저 생성
    @staticmethod
    def create_user(email='testuser@test.co.kr', nickname='testuser'):
        return User.objects.create_user(
            email=email,
            nickname=nickname,
            password='testpassword'
        )

    # 테스트 포스트 생성
    def create_post(self, user):
        API_VIEW_URL = '/post/comment/'

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