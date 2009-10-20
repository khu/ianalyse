from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from analyse.models import BuildFactory, Build

def home(request):
    return redirect('index.html')

def index(request):
    proj_name = request.GET["project"];

    context = Context({
    "total" : Build.total(proj_name),
    "project" : Build.total(proj_name)
    })
    BuildFactory.create_builds(proj_name)

    Build.analyse_all(proj_name)

    return render_to_response('analyse/index.html', context, context_instance = RequestContext(request))

