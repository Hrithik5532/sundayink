

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages #import messages

def mail_send(request,associated_users):
    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "registration/password_reset_email.txt"
                        c = {
                        "email":user.email,
                        'domain':'',
                        'site_name': 'SundayInk',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'shrenik@sundayink.in', [user.email])
                            messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                            
                        except BadHeaderError:
                            messages.error(request, 'An invalid email has been entered.')

                            return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":PasswordResetForm()})

    return redirect ("main:homepage")

