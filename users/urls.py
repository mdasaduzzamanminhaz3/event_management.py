from django.urls import path
from users.views import sign_up,sign_in,activate_user,sign_out,SignUp,SignIn,Logout,ProfileView,ChangePassword,EditProfileView,CustormPasswordResetConfirm,CustomPasswordReset
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView

urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    # path('sign-up/',SignUp.as_view(),name='sign-up'),
    # path('sign-in/',sign_in,name='sign-in'),
    path('sign-in/',SignIn.as_view(),name='sign-in'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    # path('sign-out/',sign_out,name='sign-out')
    path('sign-out/',Logout.as_view(),name='sign-out'),
    path('user/profile',ProfileView.as_view(),name='profile'),
    path('edit-profile/',EditProfileView.as_view(),name = 'edit-profile'),
    path('password-change/',ChangePassword.as_view(),name='password-change'),
    path('password-reset/',CustomPasswordReset.as_view(),name='reset-password'),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name ='accounts/password_change_done.html'),name='password_change_done'),
    path('password-reset/confirm/<uidb64>/<token>/',CustormPasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('edit-profile/',EditProfileView.as_view(),name = 'edit-profile')

]
