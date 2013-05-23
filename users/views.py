from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms

@csrf_exempt
def signin(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')

    return render_to_response('users/signin.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')
