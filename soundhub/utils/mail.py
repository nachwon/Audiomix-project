from django.core.mail import send_mail
from django.urls import reverse


def send_verification_mail(activation_key, recipient_list):
    """
    activation key 를 담은 activation_link 를 recipient 에게 보냄

    :param activation_key: activation key 의 기능을 수행하는 40자 문자열
    :param recipient_list: 수신자 이메일 목록
    :return:
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

