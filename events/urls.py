from django.urls import path
from events.views import dashboard,admin_dashboard,participant_dashboard,rsvp_event,organizar_dashboard, search,user_page,create_event,add_participant,update_event,delete_event,organizer_view,view_participants,view_event_participant,edit_participant,remove_participant,create_category,remove_category,update_category
from core.views import no_permission
urlpatterns = [
    path('search/',search,name='search'),
    path("organizar_dashboard/", organizar_dashboard,name='organizar_dashboard'),
    path('organizer_view/', organizer_view, name='organizer_view'),
    path('create_event/',create_event,name='create_event'),
    path('update_event/<int:id>/',update_event ,name='update_event'),
    path('delete_event/<int:id>/',delete_event ,name='delete_event'),
    path('add_participant/',add_participant,name="add_participant"),
    path('edit_participant/<int:id>/',edit_participant,name="edit_participant"),
    path('remove_participant/<int:id>/',remove_participant,name="remove_participant"),
    path('participants/', view_participants, name='view_participants'),
    path('user_page/', user_page, name='user_page'),
    path('view_event_participant/<int:id>/',view_event_participant,name='view_event_participant'),
    path('create_category/',create_category,name='create_category'),
    path('remove_category/<int:id>/',remove_category ,name='remove_category'),
    path('update_category/<int:id>/',update_category ,name='update_category'),
    path('no-permission/',no_permission,name='no-permission'),
    path('rsvp_event/<int:event_id>/',rsvp_event,name = 'rsvp_event'),
    path('participant_dashboard',participant_dashboard,name='participant_dashboard'),
    path('admin_dashboard',admin_dashboard,name='admin_dashboard'),
    path('dashboard/',dashboard,name='dashboard')

]