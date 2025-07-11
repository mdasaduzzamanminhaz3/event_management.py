from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from users.forms import CustomRegistrationForm,LoginForm,User
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.
def assign_user_to_group(user,role):
    group,created = Group.objects.get_or_create(name=role)
    user.groups.add(group)
def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            assign_user_to_group(user,'Participant')
            messages.success(request,'A confirmation mail sent. Pleace check your email')
            return redirect('sign-in')

    return render(request,'registration/registar.html',{"form":form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data =request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('user_page')
    return render(request,'registration/sign_in.html',{'form':form})


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    
@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')

