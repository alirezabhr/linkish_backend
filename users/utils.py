from django.core.mail import EmailMessage


def send_email(receivers, subject, body):
    msg = EmailMessage(
        subject,
        body,
        to=receivers,
    )
    msg.send()


def send_otp_email(otp, receiver):
    email_body = f'رمز یکبار مصرف لینکیش شما\n' \
                 f'{otp}\n\n' \
                 f'اگر درخواست رمز یکبار مصرف نداده اید، این ایمیل را نادیده بگیرید'

    send_email([receiver], "No Reply", email_body)


def send_withdraw_email(applicant, amount):
    email_body = f'withdraw request\n' \
                 f'applicant user: {applicant}\n' \
                 f'withdraw amount: {amount}T'
    receivers = ['alirezabahrololoom@gmail.com', 'mehdiscientist@gmail.com']

    send_email(receivers, "Withdraw", email_body)


def send_suggest_ad_email(receiver, title):
    email_body = f'تبلیغ جدید برای شما پیشنهاد شده است\n' \
                 f'عنوان تبلیغ: {title}'

    send_email([receiver], "No Reply", email_body)
