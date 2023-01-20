
from urllib import request
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import SignUpForm
from django.contrib.auth.models import User
from blogs.models import IpModel

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create your views here.
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
from .mail_send import mail_send
def homepage(request):
	return HttpResponseRedirect(reverse('home'))

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				mail_send(request,associated_users)
                

	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})

def UserRegistrationView(request):

    ip_count = IpModel.objects.all().count()

    form_class = SignUpForm()
    if request.method == "POST":
        # form = SignUpForm(request.POST)
        email = request.POST.get('email')
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if email != '' and username != '' and fname != '' and lname != '' and email != "" and pass1 != '' and pass2 != '':
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, f"{email} is already used")
                return HttpResponseRedirect(reverse('register'))
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, f" Username is already used")
                    return HttpResponseRedirect(reverse('register'))
                else:
                    if pass1 == pass2:
                        # if fname  in pass1:
                        #     messages.error(request,'Password Warning')

                        #     return HttpResponseRedirect(reverse('register'))
                        # else:
                        User.objects.create_user(
                            username=username, first_name=fname, last_name=lname, email=email, password=pass1)
                        messages.success(request, "register")
                        return HttpResponseRedirect(reverse('login'))

                    else:
                        messages.error(request, 'Enter Correct Passwords')
                        return HttpResponseRedirect(reverse('register'))
        else:
            messages.error(request, 'Please Fill Correct Information')
            return HttpResponseRedirect(reverse('register'))
    return render(request, "registration/register.html", {'form': form_class, 'ip_count': ip_count})
