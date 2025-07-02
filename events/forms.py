from django import forms
from .models import Event,Participant,Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-input p-2 border-none rounded shadow-md m-4 mt-4','placeholder':'Enter your name'}),
            'description': forms.Textarea(attrs={'rows': 3,'class':'form-textarea resize-none p-2 border-garay-300 rounded w-1/2 m-4 mt-4 shadow-md ','placeholder':'Describe your Event details'}),
            'date': forms.DateInput(attrs={'type': 'date','class':'p-2 form-input border-none shadow-md m-4 mt-4 rounded w-1/2'}),
            'time': forms.TimeInput(attrs={'type': 'time','class':'p-2 form-input border-none shadow-md m-4 mt-4 rounded w-1/2'}),
            'location': forms.Textarea(attrs={'rows': 3,'class':'form-textarea resize-none p-2 border-garay-300 shadow-md m-4 mt-4 rounded w-40','placeholder':'Enter your location'}),
            'category': forms.Select(attrs={'class':'form-textarea p-2 border-garay-300 rounded shadow-md w-40 m-4 mt-4 mb-4'}),
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields =['name','email','events']
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-input p-2 border-none rounded shadow-md m-4 mt-4','placeholder':'Enter your name'}),
            'email':forms.TextInput(attrs={'class':'form-input p-2 border-none rounded shadow-md m-4 mt-4 mb-4','placeholder':'Enter your email'}),
            'events':forms.CheckboxSelectMultiple(attrs={'class':'mb-4'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['name','description']
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-input p-2 border-none rounded shadow-md m-4 mt-4','placeholder':'type your category'}),
            'description': forms.Textarea(attrs={'rows': 3,'class':'form-textarea resize-none p-2 border-garay-300 rounded w-1/2 m-4 mt-4 shadow-md ','placeholder':'Describe your Event details'}),
        }


