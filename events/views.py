from django.shortcuts import render,redirect
from events.models import Event,Category
from .forms import EventForm,ParticipantForm,CategoryForm
from django.contrib import messages
from datetime import date
from django.db.models import Q
from django.contrib.auth.models import User ,Group
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from django.core.mail import send_mail
from django.conf import settings

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


@login_required(login_url='sign-in')
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def organizer_view(request):
    events = Event.objects.select_related('category').all()
    # print(events)
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

@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def delete_event(request,id):
    event = Event.objects.get(id=id)
    if request.method =='POST':
        event.delete()
        return redirect('organizar_dashboard')
    return render(request,"event_confirm_delete.html",{'event':event})

@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
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

@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def view_participants(request):
    participants = User.objects.all()
    return render(request,"organizar_dashboard.html",{'participants':participants})

@login_required(login_url='sign-in')
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def user_page(request):
    events = Event.objects.select_related('category').all()
    return render(request,'home.html',{"events":events})


def search(request):
    query = request.GET.get('search')
    events= Event.objects.all()
    if query:
        events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))
    else:
        events =Event.objects.all()
    return render(request,'home.html',{'events':events, 'query': query})
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

@login_required(login_url='sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def remove_participant(request,id):
    participant = User.objects.get(id=id)
    if request.method =='POST':
        participant.delete()
        return redirect('organizar_dashboard')
    return render(request,'participant_confirm_delete.html',{'participant':participant})


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

@login_required(login_url='sign-in')
@user_passes_test(is_organizer,login_url='no-permission')
def remove_category(request,id):
    category = Category.objects.get(id=id)
    if request.method=='POST':
        category.delete()
        return redirect('create_category')
    return render(request,'create_category.html',{'category':category})

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

def participant_dashboard(request):
    user = request.user
    events = Event.objects.filter(participants=user).prefetch_related('participants')
    return render(request,'participant_dashboard.html',{'events':events})

@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizar_dashboard')
    elif is_participant(request.user):
        return redirect('participant_dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')
    return redirect('no-permission')