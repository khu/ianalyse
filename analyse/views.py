from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from analyse.models import Builds, Build
from analyse.config import Config, Configs

def home(request):
    return redirect('index.html')

def index(request):
    configs = Configs()
    config = configs.find('dummy')
    proj_name = config.project_name()

    if not config.has_result(proj_name) :
        return redirect('setup.html')        

    over_all_result = {
        "project_name" : proj_name
    }
    Build.view_all(proj_name, over_all_result)                                                                  
    return render_to_response('analyse/index.html', Context(over_all_result), context_instance = RequestContext(request))

def setup(request):
    configs = Configs()
    config = configs.find('dummy')
    proj_name = config.project_name()

    over_all_result = {
        "project_name" : proj_name
    }

    config.view_all(over_all_result)
    return render_to_response('analyse/setup.html', Context(over_all_result), context_instance = RequestContext(request))

def generate(request) :
    configs = Configs()
    config = configs.find(request.POST['id'])
    proj_name = config.project_name()
    over_all_result = {
        "project_name" : proj_name
    }

    Builds.create_builds(config, None, config.builds())
    Build.analyse_all(proj_name, over_all_result)
    Builds.create_csv(proj_name)
    return redirect('index.html')

def show(request):
    project_id = request.GET['id']
    config = Configs().find(project_id)

    if not config.has_result(project_id) :
        return redirect('setup.html')

    over_all_result = {
        "project_name" : project_id,
        "type"         : 'pass_rate'
    }
    Build.view_all(project_id, over_all_result)                                                                  
    return render_to_response('analyse/show.html', Context(over_all_result), context_instance = RequestContext(request))
