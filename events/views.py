from django.shortcuts import render,redirect
from events.models import Event,Category
from .forms import EventForm,ParticipantForm,CategoryForm
from django.contrib import messages
from datetime import date
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView,UpdateView,ListView,CreateView,DetailView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.views import View
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import get_user_model

User = get_user_model()
@login_required(login_url='sign-in')
def rsvp_event(request,event_id):
    event = Event.objects.get(id = event_id)
    user = request.user
    if event.participants.filter(id=user.id).exists():
        messages.success(request,"You have already RSVP for this event.")
        return redirect('user_page')
    event.participants.add(user)
    event.save()
    subject = f"RSVP Confirmation for {event.name}"
    message = f"Hi {user.username},\n\nYou have successfully RSVPed for the event: {event.name} on {event.date}.\n\nLocation: {event.location}\n\nThank you!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    messages.success(request, f'You have successfully RSVPed for {event.name}')
    return redirect('user_page')

def is_admin_or_organizer(user):
    print("User:", user.username)
    print("Groups:", user.groups.all())

    return user.groups.filter(name__in=['Admin', 'Organizer']).exists()
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()
def is_participant(user):
    return user.groups.filter(name='Participant').exists()

@login_required(login_url='sign-in')
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    total_participants = User.objects.filter(groups__name='Participant').count()
    total_organizers = User.objects.filter(groups__name='Organizer').count()

    events = Event.objects.select_related('category').prefetch_related('participants')

    context = {
        'total_users': total_users,
        'total_events': total_events,
        'total_categories': total_categories,
        'total_participants': total_participants,
        'total_organizers': total_organizers,
        'events': events,
    }
    return render(request, 'admin_dashboard.html', context)

class AdminDashboard(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    template_name = 'admin_dashboard.html'
    login_url = reverse_lazy('sign-in')
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')
    def get(self,request,*args,**kwargs):
        total_users = User.objects.count()
        total_events = Event.objects.count()
        total_categories = Category.objects.count()
        total_participants = User.objects.filter(groups__name='Participant').count()
        total_organizers = User.objects.filter(groups__name='Organizer').count()

        events = Event.objects.select_related('category').prefetch_related('participants')

        context = {
            'total_users': total_users,
            'total_events': total_events,
            'total_categories': total_categories,
            'total_participants': total_participants,
            'total_organizers': total_organizers,
            'events': events,
        }
        return render(request, 'admin_dashboard.html', context)
    

@login_required(login_url='sign-in')
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def organizer_view(request):
    events = Event.objects.select_related('category').all()
    # print(events)
    return render(request, "organizer_view.html", {'events': events})

class OrganizerView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = reverse_lazy('sign-in')
    def test_func(self):
        return is_admin_or_organizer(self.request.user)
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')
    def get(self,request,*args,**kwargs):
        events = Event.objects.select_related('category').all()
        return render(request, "organizer_view.html", {'events': events})

@user_passes_test(is_organizer,login_url='no-permission')
def organizar_dashboard(request):
    # participants = User.objects.prefetch_related('events')
    participants = User.objects.filter(groups__name='Participant').prefetch_related('rsvp_event')

    total_participants = participants.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=date.today()).count()
    past_events = Event.objects.filter(date__lt=date.today()).count()

    context = {
        'participants': participants,
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }

    return render(request, 'organizar_dashboard.html', context)
class OrganizerDashboard(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = reverse_lazy('sign-in')

    def test_func(self):
        return is_organizer(self.request.user)
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')
    
    def get(self,request,*args,**kwargs):
        participants = User.objects.filter(groups__name='Participant').prefetch_related('rsvp_event')

        total_participants = participants.count()
        total_events = Event.objects.count()
        upcoming_events = Event.objects.filter(date__gte=date.today()).count()
        past_events = Event.objects.filter(date__lt=date.today()).count()

        context = {
            'participants': participants,
            'total_participants': total_participants,
            'total_events': total_events,
            'upcoming_events': upcoming_events,
            'past_events': past_events,
        }
        return render(request, 'organizar_dashboard.html', context)

@login_required(login_url='sign-in')
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def create_event(request):
    if request.method =='POST':
        form= EventForm(request.POST,request.FILES)
        if form.is_valid():
           event= form.save(commit=False)
           event.save()
           messages.success(request, "Created event added Sucessfully")
           return redirect('organizar_dashboard')     
    else:
        form = EventForm()
    return render(request,"event_form.html",{'form':form})


class CreateEvent(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    template_name = "event_form.html"
    model = Event
    form_class = EventForm
    login_url =reverse_lazy('sign-in')
    success_url = reverse_lazy('organizar_dashboard')
    def form_valid(self, form):
        messages.success(self.request, "Created event added Successfully")
        return super().form_valid(form)
    
    def test_func(self):
        return is_admin_or_organizer(self.request.user)
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')

@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def view_event_participant(request,id):
   event = Event.objects.get(id=id)
   participants = event.participants.all()
#    participants = Participant.objects.prefetch_related('events')
   context = {
        'event': event,
        'participants': participants
    }
   return render(request,"organizar_dashboard.html",context)

class ViewEventParticipant(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Event
    pk_url_kwarg ='id'
    template_name ="organizar_dashboard.html"
    context_object_name = 'event'
    login_url = reverse_lazy('sign-in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participants'] = self.object.participants.all()
        return context
    def test_func(self):
        return is_organizer(self.request.user)
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')


@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def update_event(request,id):
    event = Event.objects.get(id=id) 
    if request.method =='POST':
        form= EventForm(request.POST, instance=event)
        if form.is_valid():
           event= form.save(commit=False)
           event.save()
           messages.success(request, "Event Update Sucessfully")
           return redirect('organizar_dashboard')
    else:
        form = EventForm(instance=event)
    return render(request,"event_form.html",{'form':form})

class UpdateEvent(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model= Event
    pk_url_kwarg ='id'
    template_name ="event_form.html"
    form_class =EventForm
    login_url =reverse_lazy('sign-in')
    success_url = reverse_lazy('organizar_dashboard')
    def test_func(self):
        return is_admin_or_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')
    def form_valid(self, form):
        messages.success(self.request, "Event Update Sucessfully")
        return super().form_valid(form)
    
    

@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def delete_event(request,id):
    event = Event.objects.get(id=id)
    if request.method =='POST':
        event.delete()
        return redirect('organizar_dashboard')
    return render(request,"event_confirm_delete.html",{'event':event})

class DeleteEvent(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Event
    pk_url_kwarg ='id'
    login_url =reverse_lazy('sign-in')
    success_url=reverse_lazy('organizar_dashboard')
    template_name="event_confirm_delete.html"
    def test_func(self):
        return is_admin_or_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')

@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def add_participant(request):
    if request.method =='POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.is_active = True
            user.save()
            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)
            messages.success(request,"participant add sucessfully!")
            return redirect('add_participant')
    else:
        form = ParticipantForm()
    return render(request,"add_participant.html",{'form':form})

class AddParticipant(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class = ParticipantForm
    template_name ="add_participant.html"
    success_url = reverse_lazy('add_participant')
    def form_valid(self, form):
        user= form.save(commit=False)
        user.is_active = True
        user.save()
        participant_group, created = Group.objects.get_or_create(name='Participant')
        user.groups.add(participant_group)
        messages.success(self.request,"participant add sucessfully!")
        return super().form_valid(form)
    def test_func(self):
        return is_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')  

@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def view_participants(request):
    participants = User.objects.all()
    return render(request,"organizar_dashboard.html",{'participants':participants})

class ViewParticipant(LoginRequiredMixin,UserPassesTestMixin,ListView):
    template_name ="organizar_dashboard.html"
    model = User
    context_object_name='participants'
    login_url =reverse_lazy('sign-in')
    def test_func(self):
        return is_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission') 

@login_required(login_url='sign-in')
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def user_page(request):
    events = Event.objects.select_related('category').all()
    return render(request,'home.html',{"events":events})

class UserPage(LoginRequiredMixin,TemplateView):
    model = Event
    template_name ='home.html'
    login_url =reverse_lazy('sign-in')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.select_related('category').all()
        return context
    def test_func(self):
        return is_participant(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission') 
    
def search(request):
    query = request.GET.get('search')
    events= Event.objects.all()
    if query:
        events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))
    else:
        events =Event.objects.all()
    return render(request,'home.html',{'events':events, 'query': query})

class SearchEvent(ListView):
    model = Event
    template_name ='home.html'
    context_object_name = 'events'
    def get_queryset(self):
        query = self.request.GET.get('search','')
        if query:
            events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))
            return events
        return Event.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get('search','')
        return context
    

@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def edit_participant(request,id):
    participant = User.objects.get(id=id) 
    if request.method =='POST':
        form= ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
           participant= form.save(commit=True)
           participant.save()
           messages.success(request, "Participant edit Sucessfully")
           return redirect('organizar_dashboard')
    else:
        form = ParticipantForm(instance=participant)
    return render(request,"add_participant.html",{'form':form})

class EditParticipant(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = User
    form_class = ParticipantForm
    pk_url_kwarg ='id'
    login_url =reverse_lazy('sign-in')
    template_name = "add_participant.html"
    success_url = reverse_lazy('organizar_dashboard')
    def form_valid(self, form):
        messages.success(self.request, "Participant edit Sucessfully")
        return super().form_valid(form)
    def test_func(self):
        return is_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')


@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def remove_participant(request,id):
    participant = User.objects.get(id=id)
    if request.method =='POST':
        participant.delete()
        return redirect('organizar_dashboard')
    return render(request,'participant_confirm_delete.html',{'participant':participant})

class RemoveParticipant(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = User
    template_name ='participant_confirm_delete.html'
    success_url = reverse_lazy('organizar_dashboard')
    pk_url_kwarg = 'id'
    login_url =reverse_lazy('sign-in')
    def test_func(self):
        return is_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission') 

@login_required(login_url='sign-in')
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def create_category(request):
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request,"Category add sucessfully!")
            return redirect('create_category')
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request,"create_category.html",{'form':form,'categories':categories})  

class CreateCategory(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class = CategoryForm
    template_name = "create_category.html"
    success_url = reverse_lazy('create_category')
    login_url =reverse_lazy('sign-in')
    def form_valid(self, form):
        messages.success(self.request,"Category add successfully!")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] =Category.objects.all()
        return context
    def test_func(self):
        return is_admin_or_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')

@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def remove_category(request,id):
    category = Category.objects.get(id=id)
    if request.method=='POST':
        category.delete()
        return redirect('create_category')
    return render(request,'create_category.html',{'category':category})

class RemoveCategory(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Category
    pk_url_kwarg ='id'
    success_url = reverse_lazy('create_category')
    
    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)
    def test_func(self):
        return is_admin_or_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')

@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def update_category(request,id):
    category = Category.objects.get(id=id) 
    if request.method =='POST':
        form= CategoryForm(request.POST, instance=category)
        if form.is_valid():
           category= form.save(commit=False)
           category.save()
           messages.success(request, "Category Update Sucessfully")
           return redirect('create_category')
    else:
        form = CategoryForm(instance=category)
    return render(request,"create_category.html",{'form':form})

class UpdateCategory(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    pk_url_kwarg ='id'
    template_name = "create_category.html"
    success_url = reverse_lazy('create_category')
    login_url =reverse_lazy('sign-in')
    def form_valid(self, form):
        messages.success(self.request, "Category Update Sucessfully")
        return super().form_valid(form)
    def test_func(self):
        return is_admin_or_organizer(self.request.user)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        return redirect('no-permission')

def participant_dashboard(request):
    user = request.user
    events = Event.objects.filter(participants=user).prefetch_related('participants')
    return render(request,'participant_dashboard.html',{'events':events})
class ParticipantDashboard(LoginRequiredMixin,TemplateView):
    template_name ='participant_dashboard.html'
    login_url =reverse_lazy('sign-in')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        events = Event.objects.filter(participants=user).prefetch_related('participants')
        context['events'] = events
        return context 

@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizar_dashboard')
    elif is_participant(request.user):
        return redirect('participant_dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')
    return redirect('no-permission')