from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from users.forms import CustomRegistrationForm,LoginForm,CustomPasswordChangeForm,EditProfileForm,CustomPasswordResetConfirmForm,CustomPasswordResetForm
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import TemplateView,UpdateView,ListView,CreateView
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views import View
from django.contrib.auth import get_user_model

User = get_user_model()
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

class SignUp(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'registration/registar.html'
    success_url = reverse_lazy('sign-in')
    def form_valid(self,form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()
        assign_user_to_group(user,'Participant')
        messages.success(self.request,'A confirmation mail sent. Pleace check your email')
        return super().form_valid(form)



def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data =request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('user_page')
    return render(request,'registration/login.html',{'form':form})

class SignIn(LoginView):
    form_class = LoginForm
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


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

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('sign-in')
    
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['phone_number'] =user.phone_number
        context['name'] = user.get_full_name()
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        # context['bio'] = user.bio
        context['profile_image'] = user.profile_image

        return context
 
class ChangePassword(PasswordChangeView):
    template_name ='accounts/password_change.html'
    form_class = CustomPasswordChangeForm

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        # print(self.request.user.userprofile.bio)
        # print(self.request.user.userprofile.profile_image)
        return redirect('profile')
    

class CustomPasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name ='registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request,'A reset email send. please check your email.')
        return super().form_valid(form)
   
    
class CustormPasswordResetConfirm(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name ='registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request,'Password reset successfully.')
        return super().form_valid(form)

