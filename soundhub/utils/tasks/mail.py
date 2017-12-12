from django.core.mail import send_mail
from django.urls import reverse

from config import celery_app


__all__ = (
    'send_verification_mail',
    'send_confirm_readmission_mail',
    'send_verification_mail_after_social_login',
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
    # host = 'soundhub-dev.ap-northeast-2.elasticbeanstalk.com'
    host_local = 'localhost:8000'
    activation_link = scheme + host_local + reverse('user:activate') + f'?activation_key={activation_key}'

    subject = '[Soundhub] Email Verification'
    message = f'Verify your email to login Soundhub \n: {activation_link}'
    from_email = 'joo2theeon@gmail.com'
    return send_mail(
        subject=subject,
        message=message,
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
    host_local = 'localhost:8000'
    # data 에 전달된 값을 get parameter 로 재구성
    params = '?'
    for key, value in data.items():
        params = params + f'{key}={value}&'
    # 완성된 회원가입 링크
    signup_link = scheme + host_local + reverse('user:signup') + params[:-1]

    subject = '[Soundhub] Email Verification (Signup Soundhub after social login)'
    message = f"Verify your email to login Soundhub \n: {signup_link}"
    from_email = 'joo2theeon@gmail.com'
    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
