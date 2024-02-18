from django import forms
from .models import Review
from users.models import Contact

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'