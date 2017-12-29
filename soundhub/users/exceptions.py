from rest_framework import status
from rest_framework.exceptions import APIException


# request 에 필요한 데이터가 오지 않았을 때
class RequestDataDoesNotExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Necessary data does not exist, check data in your request.'


# Unique 해야 하는 필드가 중복될 때
class UniqueFieldDuplication(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Duplicated data were given in unique field.'


# request 로 전달된 데이터가 유효하지 않을 때
class RequestDataInvalid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid data were given.'
