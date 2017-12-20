from django.core.mail import send_mail
from django.urls import reverse

from config import celery_app


__all__ = (
    'send_verification_mail',
    'send_confirm_readmission_mail',
    'send_verification_mail_after_social_login',
    'send_password_reset_mail',
)


@celery_app.task
def send_verification_mail(activation_key, recipient_list):
    """
    activation key 를 담은 activation_link 를 recipient 에게 보냄

    :param activation_key: activation key 의 기능을 수행하는 40자 문자열
    :param recipient_list: 수신자 이메일 목록 list 객체
    :return: send_mail 함수 반환 값
    """
    scheme = 'http://'
    # 배포용 서버
    # host = 'soundhub-dev.ap-northeast-2.elasticbeanstalk.com'
    # 테스트용 서버
    host = 'localhost:8000'
    activation_link = scheme + host + reverse('user:activate') + f'?activation_key={activation_key}'

    subject = '[Soundhub] Email Verification'
    message = ''
    html_message = f'Verify your email to login Soundhub: <a href="{activation_link}">activation link</a>'
    from_email = 'joo2theeon@gmail.com'
    return send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
    )


@celery_app.task
def send_confirm_readmission_mail(recipient_list):
    """
    아직 이메일 인증이 이루어지지 않은 메일로 새로운 가입 요청이 왔을 때 보내주는 알림 메일

    :param recipient_list: 리스트 타입 수신자 목록
    :return: send_mail 함수 반환 값
    """
    subject = '[Soundhub] Confirmation of Readmission'
    message = "Someone tried to signup with your email."
    from_email = 'joo2theeon@gmail.com'
    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )


@celery_app.task
def send_verification_mail_after_social_login(data, recipient_list):
    """
    소셜로그인을 했다가 일반 회원가입을 다시 요청한 변태 가입자를 위한 안내 메일

    :param data: 회원 가입에 필요한 정보 dictionary 객체
    :param recipient_list: 수신자 email list 객체
    :return: send_mail 함수 반환 값
    """
    scheme = 'http://'
    # host = 'soundhub-dev.ap-northeast-2.elasticbeanstalk.com'
    host = 'localhost:8000'

    # data 에 전달된 값을 get parameter 로 재구성
    # params = '?key=value&key=value&' 형태
    params = '?'
    for key, value in data.items():
        params = params + f'{key}={value}&'

    # 완성된 회원가입 링크
    signup_link = scheme + host + reverse('user:signup') + params[:-1]  # params[:-1]은 맨 뒤에 &를 떼는 로직

    subject = '[Soundhub] Email Verification (Signup Soundhub after social login)'
    message = ''  # 메세지는 필수 필드
    html_message = f'Verify your email to login Soundhub: <a href="{signup_link}">signup link</a>'
    from_email = 'joo2theeon@gmail.com'
    return send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
    )


@celery_app.task
def send_password_reset_mail(data, recipient_list):
    """
    비밀번호가 변경되었음을 알리는 메일. 본인이 한 것이 아닐 경우, 다시 변경할 수 있는 링크가 걸려있다.

    :param data: 비밀번호 변경에 필요한 정보 dictionary 객체
    :param recipient_list: 수신자 email list 객체
    :return: send_mail 함수 반환 값
    """
    scheme = 'http://'
    # host = 'soundhub-dev.ap-northeast-2.elasticbeanstalk.com'
    host = 'localhost:8000'

    # data 에 전달된 값을 get parameter 로 재구성
    # params = '?key=value&key=value&' 형태
    params = '?'
    for key, value in data.items():
        params = params + f'{key}={value}&'

    # 완성된 패스워드 변경 링크
    reset_password_link = scheme + host + reverse('user:password') + params[:-1]  # params[:-1]은 맨 뒤에 &를 떼는 로직

    subject = '[Soundhub] Reset Password Link  (Signup Soundhub after social login)'
    message = ''  # 메세지는 필수 필드
    html_message = f'Verify your email to reset password in Soundhub: ' \
                   f'<a href="{reset_password_link}">reset password link</a>'
    from_email = 'joo2theeon@gmail.com'
    return send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
