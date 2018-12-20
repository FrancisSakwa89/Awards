from django import forms

from .models import Profile, Project, Rating

class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    exclude = ['poster','postername', 'pub_date']


class RatingForm(forms.ModelForm):
  class Meta:
    model = Rating
    exclude = ['average','project','postername','pub_date']


class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['user']

class AwardLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')    