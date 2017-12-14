from django.conf import settings
from django.db.models.fields.files import ImageFieldFile, ImageField

__all__ = (
    'DefaultStaticImageField',
)


# 커스텀 이미지 필드 파일
class DefaultStaticImageFieldFile(ImageFieldFile):
    # 파일의 url 메서드를 호출 했을 때
    @property
    def url(self):
        # 파일 필드에 파일이 있으면 원래 url 메서드 실행
        try:
            return super().url
        # 없으면 ValueError 가 발생함
        except ValueError:
            # 에러 발생시 /static/ 경로에서부터 시작하는 staticfiles_storage 저장소 객체를 불러옴
            from django.contrib.staticfiles.storage import staticfiles_storage
            # self.field 로 DefaultStaticImageField 객체에 접근해서
            # static_image_path 값을 가져온 다음,
            # /static/ 에 이어 붙여서 url 생성한 다음 리턴
            return staticfiles_storage.url(self.field.static_image_path)


# 커스텀 모델 이미지 필드
class DefaultStaticImageField(ImageField):
    # 파일은 커스텀 이미지 필드 파일을 사용
    attr_class = DefaultStaticImageFieldFile

    # 모델에서 정의될 때 default 에 정해준 경로 있으면 가져옴
    # 없으면 settings 의 DEFAULT_IMAGE_PATH 가져옴
    # 그것마저도 없으면 default-profile.png 를 가져옴
    # 거져온 값을 static_image_path 라는 변수에 저장
    def __init__(self, *args, **kwargs):
        self.static_image_path = kwargs.pop(
            'default',
            getattr(settings, 'DEFAULT_IMAGE_PATH', 'default-profile.png'))
        super().__init__(*args, **kwargs)
