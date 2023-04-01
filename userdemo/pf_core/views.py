
from django.shortcuts import render, redirect

from django.template import loader

from django.http import HttpResponse

from django.contrib.auth import logout



def home(request):
    
    return render(request, 'pf_core/home.html')



def logout_view(request):

    logout(request)

    if hasattr(request, 'pf_core_context'):
        delattr(request, 'pf_core_context')
    
    return redirect('home')
