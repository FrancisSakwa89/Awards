from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
def welcome(request):
    return render (request,'index.html')
