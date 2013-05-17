from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from layers.models import Layer
from django.conf import settings
from safe.api import read_layer
import glob
import os

def index(request):
    layers = Layer.objects.all()
    context = { 'layers': layers }
    return render(request, 'layers/index.html', context)

def detail(request, layer_slug):
    layer = get_object_or_404(Layer, slug=layer_slug)
    return render(request, 'layers/detail.html', {'layer': layer})

def get_layer_data(layer_name):
     layer = Layer.objects.get(name=layer_name)
     layer_path = os.path.join(settings.MEDIA_ROOT, 'layers', layer.slug, 'raw')
     os.chdir(layer_path)
     filename = glob.glob('*.shp')[0]
     layer_file = os.path.join(layer_path, filename)
     return read_layer(layer_file)

def calculate(request):
     """Calculates the buildings affected by flood.
     """
     buildings = get_layer_data('Buildings')
     flood = get_layer_data('Flood')
     return HttpResponse('<ul><li>' 
                         + buildings.filename
                         + '</li><li>'
                         + flood.filename
                         + '</li></ul>')
