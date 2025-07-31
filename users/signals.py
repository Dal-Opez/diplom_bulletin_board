from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном при запросе сброса пароля
    """
    print(f"\n=== ТОКЕН ДЛЯ {reset_password_token.user.email} ===")  # Вывод в консоль
    print(f"Токен: {reset_password_token.key}\n")  # Вывод в консоль

    # Отправка письма
    context = {
        "current_user": reset_password_token.user,
        "token": reset_password_token.key,
    }

    email_html_message = render_to_string(
        "users/email/password_reset_email.html", context
    )
    email_plaintext_message = f"Ваш токен для сброса пароля: {reset_password_token.key}"

    msg = EmailMultiAlternatives(
        subject="Сброс пароля",
        body=email_plaintext_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
