# Create your views here.
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from analyse.models import *


def index(request):
    builds = BuildFactory.create_builds();
    context = Context({
        "total" : len(Build.objects.all())
    })
    return render_to_response('analyse/index.html', context, context_instance = RequestContext(request))

