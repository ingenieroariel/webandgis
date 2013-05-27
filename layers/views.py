from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from layers.models import Layer
from django.conf import settings
from safe.api import read_layer
from safe.api import calculate_impact
from safe.impact_functions.inundation.flood_OSM_building_impact \
    import FloodBuildingImpactFunction
from subprocess import call
import glob
import os
from django.contrib.auth.decorators import login_required


def index(request):
    layers = Layer.objects.all()
    context = {'layers': layers}
    return render(request, 'layers/index.html', context)


def detail(request, layer_slug):
    layer = get_object_or_404(Layer, slug=layer_slug)

    #get GeoJSON file
    layer_folder = os.path.join(settings.MEDIA_URL, 'layers', layer_slug)
    geometryJSON = os.path.join(layer_folder, 'raw', 'geometry.json')
    context = {'layer': layer}
    context['geojson'] = geometryJSON

    return render(request, 'layers/detail.html', context)


def get_layer_data(layer_name):
    layer = Layer.objects.get(name=layer_name)
    layer_path = os.path.join(settings.MEDIA_ROOT, 'layers', layer.slug, 'raw')
    os.chdir(layer_path)
    filename = glob.glob('*.shp')[0]
    layer_file = os.path.join(layer_path, filename)
    return read_layer(layer_file)


@login_required(redirect_field_name='next')
def calculate(request):
    """Calculates the buildings affected by flood.
    """

    output = os.path.join(settings.MEDIA_ROOT, 'layers', 'impact.json')

    buildings = get_layer_data('Buildings')
    flood = get_layer_data('Flood')

    # assign the required keywords for inasafe calculations
    buildings.keywords['category'] = 'exposure'
    buildings.keywords['subcategory'] = 'structure'
    flood.keywords['category'] = 'hazard'
    flood.keywords['subcategory'] = 'flood'

    impact_function = FloodBuildingImpactFunction
    # run analisys
    impact_file = calculate_impact(
        layers=[buildings, flood],
        impact_fcn=impact_function
    )

    call(['ogr2ogr', '-f', 'GeoJSON',
          output, impact_file.filename])

    impact_geojson = os.path.join(settings.MEDIA_URL, 'layers', 'impact.json')

    context = impact_file.keywords
    context['geojson'] = impact_geojson
    context['user'] = request.user

    return render(request, 'layers/calculate.html', context)
