from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
def welcome(request):
    # posts= PostedSite.objects.all(),
    return render(request,'index.html')


class ProjectList(APIView):
  def get(self, request, format=None):
    all_projects = Project.objects.all()
    serializers = ProjectSerializer(all_projects, many=True)
    return Response(serializers.data)

def mail(request):
  name = request.user.username
  email = request.user.email
  
  send_welcome_email(name,email)

  return HttpResponseRedirect(reverse('homepage'))

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
    return redirect('homepage')

  else:
    form = NewProjectForm()

  return render(request, 'newproject.html',{'form':form,'profile':profile})

@login_required(login_url='/accounts/login/')
def newrating(request,id):
  ida = request.user.id
  profile = Profile.objects.get(user=ida)
  idd = id

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

  return render(request, 'newrating.html',{'form':form,'profile':profile,'idd':idd})



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
