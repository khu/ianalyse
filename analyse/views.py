from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from analyse.models import BuildFactory, Build

def home(request):
    return redirect('index.html')

def index(request):
    proj_name = request.GET["project"];
    
    #BuildFactory.create_builds(proj_name)

    over_all_result = {
        "project_name" : proj_name
    }
    Build.analyse_all(proj_name, over_all_result)
    return render_to_response('analyse/index.html', Context(over_all_result), context_instance = RequestContext(request))

