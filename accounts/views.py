from django.shortcuts import render,redirect
from .forms import SignupForm,ActivateForm
from django.core.mail import send_mail
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.

def signup(request):
    '''
    - create new user
    - stop activate this code
    - send email to this user
    - redirect activate code html
    '''
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            user=form.save(commit=False)
            user.is_active=False

            form.save()  # create new user and create new profile
            profile=Profile.objects.get(user__username=username)
            # send email to this user
            send_mail(
                "Actiavte Code",
                f"Welcome Mr {username}\n pls use this code{profile.code}",
                "r_mido99@yahoo.com",
                [email],
                fail_silently=False,
                    )
            return redirect(f'/accounts/{username}/activate_code')

        

    else:
        form=SignupForm()
    return render(request,'accounts/signup.html',{'form':form})

def activate_code(request,username):
    '''
    - check code if code= profile.code
    - active this user
    - redirect login
    '''
    profile=Profile.objects.get(user__username=username)
    if request.method=='POST':
        form=ActivateForm(request.POST)
        if form.is_valid():
            code=form.cleaned_data['code']
            if code==profile.code:
                profile.code=''

                user=User.objects.get(username=username)
                user.is_active=True
                user.is_staff=True
                user.save()
                profile.save()

                return redirect('/accounts/login')

    else:
        form=ActivateForm()
    return render(request,'accounts/activate_code.html',{'form':form})
