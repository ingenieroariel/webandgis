from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from layers.models import Layer

def index(request):
    layers = Layer.objects.all()
    context = { 'layers': layers }
    return render(request, 'layers/index.html', context)

def detail(request, layer_slug):
    layer = get_object_or_404(Layer, slug=layer_slug)
    return render(request, 'layers/detail.html', {'layer': layer})
