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
    Build.analyse(proj_name).generate_chart()

    stat  = Build.analyse_x(proj_name)
    stat.generate_successful_rate_chart()
    stat.generate_build_times_chart()
    return render_to_response('analyse/index.html', context, context_instance = RequestContext(request))

