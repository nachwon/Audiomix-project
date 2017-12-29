from django.contrib.auth import get_user_model

from users.models import FacebookUserInfo

User = get_user_model()


# facebook user id 와 일치하는 유저 반환
class FacebookBackend:
    def authenticate(self, request, facebook_user_id):
        try:
            return FacebookUserInfo.objects.get(facebook_user_id=facebook_user_id).user
        except User.DoesNotExist:
            return None

    # 강사님도 아직까지 왜 이 메서드가 필요한지 모르겠다고 함. 문서에서 하라니 하는 것.
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None