from django.shortcuts import render,redirect
from events.models import Event,Participant,Category
from .forms import EventForm,ParticipantForm
from django.contrib import messages
from datetime import date
from django.db.models import Q

def admin_dashboard(request):
    events = Event.objects.select_related('category').all()
    # print(events)
    return render(request, "admin_dashboard.html", {'events': events})

def organizar_dashboard(request):
    participants = Participant.objects.prefetch_related('events')
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


def create_event(request):
    if request.method =='POST':
        form= EventForm(request.POST)
        if form.is_valid():
           event= form.save(commit=False)
           event.save()
           messages.success(request, "Created event added Sucessfully")
           return redirect('admin_dashboard')     
    else:
        form = EventForm()
    return render(request,"event_form.html",{'form':form})

def view_event_participant(request,id):
   event = Event.objects.get(id=id)
#    participants = event.participants.all()
   participants = Participant.objects.prefetch_related('events')
   context = {
        'event': event,
        'participants': participants
    }
   return render(request,"organizar_dashboard.html",context)

def update_event(request,id):
    event = Event.objects.get(id=id) 
    if request.method =='POST':
        form= EventForm(request.POST, instance=event)
        if form.is_valid():
           event= form.save(commit=False)
           event.save()
           messages.success(request, "Event Update Sucessfully")
           return redirect('admin_dashboard')
    else:
        form = EventForm(instance=event)
    return render(request,"event_form.html",{'form':form})
def delete_event(request,id):
    event = Event.objects.get(id=id)
    if request.method =='POST':
        event.delete()
        return redirect('admin_dashboard')
    return render(request,"event_confirm_delete.html",{'event':event})


def add_participant(request):
    if request.method =='POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant= form.save(commit=True)
            participant.save()
            messages.success(request,"participant add sucessfully!")
            return redirect('add_participant')
    else:
        form = ParticipantForm()
    return render(request,"add_participant.html",{'form':form})

def view_participants(request):
    participants = Participant.objects.all()
    return render(request,"organizar_dashboard.html",{'participants':participants})
def user_page(request):
    events = Event.objects.select_related('category').all()
    return render(request,'base.html',{"events":events})


def search(request):
    query = request.GET.get('search')
    events= Event.objects.all()
    if query:
        events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))
    else:
        events =Event.objects.all()
    return render(request,'base.html',{'events':events, 'query': query})

def edit_participant(request,id):
    participant = Participant.objects.get(id=id) 
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


def remove_participant(request,id):
    participant = Participant.objects.get(id=id)
    if request.method =='POST':
        participant.delete()
        return redirect('organizar_dashboard')
    return render(request,'participant_confirm_delete.html',{'participant':participant})