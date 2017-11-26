from rest_framework import permissions


# 본인의 계정은 본인만 삭제 가능
# 다른 사람의 계정은 보기만 가능
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # 안전한 요청인 경우 True
        if request.method in permissions.SAFE_METHODS:
            return True

        # 안전한 요청이 아닐 경우 해당 유저와 현재 로그인한 유저의 이메일이 일치하는지 확인
        return view.get_object() == request.user
