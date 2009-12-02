from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from analyse.models import Builds, Build
from analyse.config import Config, Configs
from django.utils.http import urlquote

def home(request):
    return redirect('index.html')

def index(request):
    configs = Configs()
    if (configs.is_empty()) :
        return render_to_response('analyse/hint.html', Context({}), context_instance = RequestContext(request))
        
    results = {'configs' : configs}
    
    return render_to_response('analyse/index.html', Context(results), context_instance = RequestContext(request))

def setup(request):
    configs = Configs()
    if (configs.is_empty()) :
        return render_to_response('analyse/hint.html', Context({}), context_instance = RequestContext(request))

    current = configs.find(request.GET.get('id'))
    results = {"configs" : configs, 'current' : current}
    return render_to_response('analyse/setup.html', Context(results), context_instance = RequestContext(request))

def generate(request) :
    configs = Configs()
    if (configs.is_empty()) :
        return render_to_response('analyse/hint.html', Context({}), context_instance = RequestContext(request))

    config = configs.find(request.POST['id'])
    over_all_result = {}
    Builds.create_builds(config, None, config.builds())
    Build.analyse_all(config.id, over_all_result)
    Builds.create_csv(config.id)
    return redirect('index.html')

def show(request):
    configs = Configs()
    if (configs.is_empty()) :
        return render_to_response('analyse/hint.html', Context({}), context_instance = RequestContext(request))
    project_id = request.GET['id']
    config = configs.find(project_id)

    if not config.has_result() :
        return redirect('setup.html?id=' + urlquote(project_id))

    over_all_result = {
        "project_id" : project_id,
    }
    Build.view_all(project_id, over_all_result)                                                                  
    return render_to_response('analyse/show.html', Context(over_all_result), context_instance = RequestContext(request))

def help(request):
    configs = Configs()
    results = {
        "configs" : configs,
    }
    return render_to_response('analyse/help.html', Context(results), context_instance = RequestContext(request))
    
    
    
    