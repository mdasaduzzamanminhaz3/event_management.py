from django.urls import path
from users.views import sign_up,sign_in,activate_user,sign_out
urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    path('sign-in/',sign_in,name='sign-in'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('sign-out/',sign_out,name='sign-out')
]
