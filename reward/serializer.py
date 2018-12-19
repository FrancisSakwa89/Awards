from rest_framework import serializers
from .models import Profile, Project


class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = ('title','image','description','link','poster','postername','pub_date')


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('profpic','bio','contact','user')