from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from analyse.models import BuildFactory, Build
from analyse.openFlashChart import Chart

def generate_chart():
    chart = Chart()

    element1 = Chart()
    element1.values =  [19,17,19,19,17,19,17,17,14,14,17,160]
    element1.type = "line"
    element1.dot_style.type = "dot"
    element1.dot_style.dot_size = 5
    element1.dot_style.colour = "#DFC329"
    element1.width = 4
    element1.colour = "#DFC329"
    element1.text = "Line 1"
    element1.font_size = 10

    element2 = Chart()
    element2.values = [112,10,8,10,13,9,8,10,8,10,10,8]
    element2.type = "line"
    element2.dot_style.type = "star"
    element2.dot_style.dot_size = 5
    element2.width = 1
    element2.colour = "#6363AC"
    element2.text = "Line 2"
    element2.font_size = 10

    element3 = Chart()
    element3.values = [7,6,2,6,6,4,3,2,5,4,2,45]
    element3.type = "line"
    element3.width = 1
    element3.colour = "#5E4725"
    element3.text = "Line 3"
    element3.font_size = 10

    # Create chart
    chart = Chart()
    chart.y_axis.min = 0
    chart.y_axis.max = 20
    chart.y_axis.font_size = 10
    chart.title.text = "Three lines example"

    #
    # here we add our data sets to the chart:
    #
    chart.elements = [element1, element2, element3]

    f = open("/Users/twer/Workspace/ianalyse/results/area-2.txt", 'w')
    try:
        f.write(chart.create())
    finally:
        f.close()

def index(request):
    builds = BuildFactory.create_builds();
    context = Context({
    "total" : Build.total('connectfour4'),
    "pass_rate" : Build.pass_rate('connectfour4')
    })

    generate_chart()
    return render_to_response('analyse/index.html', context, context_instance = RequestContext(request))