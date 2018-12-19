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
