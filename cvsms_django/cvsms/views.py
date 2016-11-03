from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def show(request):
    return render(request, 'homepage.html', {})
    #return HttpResponse("Hello World")
    #render(request, 'homepage.html', {})
