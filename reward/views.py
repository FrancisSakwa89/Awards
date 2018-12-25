from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import ProjectForm, RatingForm, ProfileForm
from .models import Project, Rating, Profile,AwardLetterRecipients
from .email import send_welcome_email
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer, ProfileSerializer
from .forms import AwardLetterForm

# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
  id = request.user.id
  profile = Profile.objects.get(user=id)

  projects = Project.objects.all().order_by('-pub_date')

  return render(request, 'index.html',{'projects':projects,'profile':profile})


@login_required(login_url='/accounts/login/')
def myprojects(request):
  id = request.user.id
  profile = Profile.objects.get(user=id)

  projects = Project.objects.all().order_by('-pub_date')

  return render(request, 'myproject.html',{'projects':projects,'profile':profile})



class ProjectList(APIView):
  def get(self, request, format=None):
    all_projects = Project.objects.all()
    serializers = ProjectSerializer(all_projects, many=True)
    return Response(serializers.data)

def mail(request):
  name = request.user.username
  email = request.user.email
  
  send_welcome_email(name,email)

  return HttpResponseRedirect(reverse('welcome'))

@login_required(login_url='/accounts/login/')
def newproject(request):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)

  current_user = request.user
  current_username = request.user.username

  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.poster = current_user
      project.postername = current_username
      project.save()
    return redirect('welcome')

  else:
    form = ProjectForm()

  return render(request, 'newproject.html',{'form':form,'profile':profile})

@login_required(login_url='/accounts/login/')
def newrating(request,id):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)
  id = id

  current_username = request.user.username

  if request.method == 'POST':
    form = RatingForm(request.POST)
    if form.is_valid():
      rating = form.save(commit=False)

      design_rating = form.cleaned_data['design']
      usability_rating = form.cleaned_data['usability']
      content_rating = form.cleaned_data['content']

      avg = ((design_rating + usability_rating + content_rating)/3)

      rating.average = avg
      rating.postername = current_username
      rating.project = Project.objects.get(pk=id)

      rating.save()
    return redirect('project',id)

  else:
    form = RatingForm()

  return render(request, 'rating.html',{'form':form,'profile':profile,'id':id})

@login_required(login_url='/accounts/login/')
def profile(request, id):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)

  user = request.user
  

  projects = Project.objects.filter(poster=frank).order_by('-pub_date')
  projectcount=projects.count()


  return render(request, 'photos/profile.html',{'profile':profile,'user':user,'projectcount':projectcount,'projects':projects})


@login_required(login_url='/accounts/login/')
def project(request, id):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)
  
  project = Project.objects.get(pk=id)
  ratings = Rating.objects.filter(project=id)

  
  project = Project.objects.get(pk=id)

  a = Rating.objects.filter(project=id).aggregate(Avg('design'))
  b = Rating.objects.filter(project=id).aggregate(Avg('usability'))
  c = Rating.objects.filter(project=id).aggregate(Avg('content'))
  d = Rating.objects.filter(project=id).aggregate(Avg('average'))
  


  return render(request, 'photos/project.html',{'profile':profile,'project':project,'ratings':ratings,'a':a,'b':b,'c':c,'d':d})



@login_required(login_url='/accounts/login/')
def newprofile(request):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)
  # current_user = request.user
  # current_username = request.user.username
  
  if request.method == 'POST':
    instance = get_object_or_404(Profile, user=frank)
    form = ProfileForm(request.POST, request.FILES,instance=instance)
    if form.is_valid():
      form.save()
      # u_profile = form.save(commit=False)
      # u_profile.user = current_user
      # u_profile.save()

    return redirect('profile', frank)

  else:
    form = ProfileForm()

  return render(request, 'newprofile.html',{'form':form,'profile':profile})


@login_required(login_url='/accounts/login/')
def search_results(request):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)


  if 'project' in request.GET and request.GET['project']:
    search_term = request.GET.get('project')
    message = f'{search_term}'
    title = 'Search Results'

    try:
      no_ws = search_term.strip()
      searched_project = Project.objects.filter(title__icontains = no_ws)

    except ObjectDoesNotExist:
      searched_projects = []

    return render(request, 'search.html',{'message':message ,'title':title, 'searched_project':searched_project,'profile':profile})

  else:
    message = 'You haven\'t searched for any Project'
    
    title = 'Search Error'
    return render(request,'search.html',{'message':message,'title':title,'profile':profile})


@login_required(login_url='/accounts/login/')
def contact(request):
  id = request.user.id
  profile = Profile.objects.get(user=id)

  return render(request, 'contacts.html', {'profile':profile})

@login_required(login_url='/accounts/login/')
def subscribe(request):
    id = request.user.id
    profile = Profile.objects.get(user=id)
    if request.method == 'POST':
        form = AwardLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = AwardLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('index.html')
    else:
        form = AwardLetterForm()
    return render(request, 'subscribe.html', {'letterForm':form,'profile':profile})    