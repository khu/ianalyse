from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from analyse.models import BuildFactory, Build



def index(request):
    builds = BuildFactory.create_builds('connectfour4');
    context = Context({
    "total" : Build.total('connectfour4')
    })
    Build.analyse('connectfour4').generate_chart()

    return render_to_response('analyse/index.html', context, context_instance = RequestContext(request))