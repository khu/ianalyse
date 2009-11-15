from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from analyse.models import Builds, Build
from analyse.config import Config

def home(request):
    return redirect('index.html')

def index(request):
    config = Config()
    proj_name = config.project_name()

    print "[" + proj_name +"]"
    print config.has_result(proj_name)
    
    over_all_result = {
        "project_name" : proj_name
    }
    config.view_all(over_all_result)    
    if config.has_result(proj_name) :
        Build.view_all(proj_name, over_all_result)                                                                  
        return render_to_response('analyse/index.html', Context(over_all_result), context_instance = RequestContext(request))
    else :
        return render_to_response('analyse/setup.html', Context(over_all_result), context_instance = RequestContext(request))


def generate(request) :
    config = Config()
    proj_name = config.project_name()
    over_all_result = {
        "project_name" : proj_name
    }
    Builds.create_builds()
    Build.analyse_all(proj_name, over_all_result)
    Builds.create_csv(proj_name)
    return redirect('index.html')

