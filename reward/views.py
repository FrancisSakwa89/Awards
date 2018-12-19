from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
  id = request.user.id
  profile = Profile.objects.get(user=id)

  projects = Project.objects.all().order_by('-pub_date')

  return render(request, 'index.html',{'projects':projects,'profile':profile})



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

def newproject(request):
  ida = request.user.id
  profile = Profile.objects.get(user=ida)

  current_user = request.user
  current_username = request.user.username

  if request.method == 'POST':
    form = NewProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.poster = current_user
      project.postername = current_username
      project.save()
    return redirect('welcome')

  else:
    form = NewProjectForm()

  return render(request, 'project.html',{'form':form,'profile':profile})

@login_required(login_url='/accounts/login/')
def newrating(request,id):
  ida = request.user.id
  profile = Profile.objects.get(user=ida)
  id = id

  current_username = request.user.username

  if request.method == 'POST':
    form = NewRatingForm(request.POST)
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
    form = NewRatingForm()

  return render(request, 'rating.html',{'form':form,'profile':profile,'id':id})

@login_required(login_url='/accounts/login/')
def profile(request, id):
  frank = request.user.id
  profile = Profile.objects.get(user=frank)

  user = request.user
  
  myprofile = Profile.objects.get(pk=id)

  projects = Project.objects.filter(poster=frank).order_by('-pub_date')
  projectcount=projects.count()


  return render(request, 'profile.html',{'profile':profile,'myprofile':myprofile,'user':user,'projectcount':projectcount,'projects':projects})


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
  


  return render(request, 'project.html',{'profile':profile,'project':project,'ratings':ratings,'a':a,'b':b,'c':c,'d':d})



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

  return render(request, 'profile.html',{'form':form,'profile':profile})


def contact(request):
    return render(request, 'contacts.html')

def search_results(request):
    if 'searchItem' in request.GET and request.GET["searchItem"]:
        search_term = request.GET.get("searchItem")
        searched_project = PostedSite.search_by_site(search_term)
        # user = User.objects.get(username=searched_user)
        # user_images = Profile.objects.get(user=searched_user)
        message = f"{search_term}"
        context = {
            'message': message,
            'projects': searched_project
        }
        return render(request, 'search.html', context)

    else:
        message.success(request, f"You haven't searched for any term")

        return render(request, 'search.html',{"message":message})
