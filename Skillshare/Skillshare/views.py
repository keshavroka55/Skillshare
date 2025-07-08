from django.shortcuts import render
from django.db.models import Q
from core.models import UserProfile


def home(request):
    return render(request,'home.html')


def success(request):
    return render(request,'login_success.html')

# def search_profile(request):
#     print("Keshav User profile is called!")
#     query = request.GET.get('q')
#     results = []

#     if query:
#         results =  UserProfile.objects.filter(
#         skills_i_have__icontains=query
#     )
#     if request.user.is_authenticated:
#         results = results.exclude(user= request.user) # exclude the search user.
#     return render(request,'search_results.html',{'results':results,'query':query})



