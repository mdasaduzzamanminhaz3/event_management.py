from django import forms
from .models import Event,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class StyledFormMixin:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })




class EventForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category','asset']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-input p-2 border-none rounded shadow-md m-4 mt-4','placeholder':'Enter your name'}),
            'description': forms.Textarea(attrs={'rows': 3,'class':'form-textarea resize-none p-2 border-garay-300 rounded w-1/2 m-4 mt-4 shadow-md ','placeholder':'Describe your Event details'}),
            'date': forms.DateInput(attrs={'type': 'date','class':'p-2 form-input border-none shadow-md m-4 mt-4 rounded w-1/2'}),
            'time': forms.TimeInput(attrs={'type': 'time','class':'p-2 form-input border-none shadow-md m-4 mt-4 rounded w-1/2'}),
            'location': forms.Textarea(attrs={'rows': 3,'class':'form-textarea resize-none p-2 border-garay-300 shadow-md m-4 mt-4 rounded w-40','placeholder':'Enter your location'}),
            'category': forms.Select(attrs={'class':'form-textarea p-2 border-garay-300 rounded shadow-md w-40 m-4 mt-4 mb-4'}),
        }

class ParticipantForm(StyledFormMixin,UserCreationForm):
    class Meta:
        model = User
        fields =['username','email','password1','password2']
        widgets ={
            'username':forms.TextInput(attrs={'class':'form-input p-2 border-none rounded shadow-md m-4 mt-4','placeholder':'Enter your name'}),
            'email':forms.TextInput(attrs={'class':'form-input p-2 border-none rounded shadow-md m-4 mt-4 mb-4','placeholder':'Enter your email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input p-2 border-none rounded shadow-md m-4 mt-4', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input p-2 border-none rounded shadow-md m-4 mt-4', 'placeholder': 'Confirm password'}),
        }
    def __init__(self, *arg, **kwarg):
        super(ParticipantForm,self).__init__(*arg, **kwarg)

        for fieldname in ['username','email','password1','password2']:
            self.fields[fieldname].help_text = None

class CategoryForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields =['name','description']
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-input p-2 border-none rounded shadow-md m-4 mt-4','placeholder':'type your category'}),
            'description': forms.Textarea(attrs={'rows': 3,'class':'form-textarea resize-none p-2 border-garay-300 rounded w-1/2 m-4 mt-4 shadow-md ','placeholder':'Describe your Event details'}),
        }



class EventParticipantForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['participants']
        widgets = {
                'participants': forms.CheckboxSelectMultiple(attrs={'class': 'mb-4'})
            }