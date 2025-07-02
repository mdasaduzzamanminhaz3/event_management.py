from django.urls import path
from events.views import organizar_dashboard, search,user_page,create_event,add_participant,update_event,delete_event,admin_dashboard,view_participants,view_event_participant,edit_participant,remove_participant

urlpatterns = [
    path('search/',search,name='search'),
    path("organizar_dashboard/", organizar_dashboard,name='organizar_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('create_event/',create_event,name='create_event'),
    path('update_event/<int:id>/',update_event ,name='update_event'),
    path('delete_event/<int:id>/',delete_event ,name='delete_event'),
    path('add_participant/',add_participant,name="add_participant"),
    path('edit_participant/<int:id>/',edit_participant,name="edit_participant"),
    path('remove_participant/<int:id>/',remove_participant,name="remove_participant"),

    path('participants/', view_participants, name='view_participants'),
    path('user_page/', user_page, name='user_page'),
    path('view_event_participant/<int:id>/',view_event_participant,name='view_event_participant'),

]