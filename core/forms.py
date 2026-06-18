from django import forms
from django.contrib.auth.models import User
from .models import Project, Bid

class SignupForm(forms.ModelForm):
    role = forms.ChoiceField(choices=(('client', 'Client'), ('freelancer', 'Freelancer')), widget=forms.RadioSelect)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'budget']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount', 'proposal']