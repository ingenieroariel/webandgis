import glob
import os

from django.shortcuts import render, get_object_or_404
from layers.models import Layer
from django.conf import settings
from safe.impact_functions.inundation.flood_polygon_roads import FloodVectorRoadsExperimentalFunction
from subprocess import call
from django.contrib.auth.decorators import login_required
from safe_qgis.utilities.qgis_layer_wrapper import QgisWrapper
from safe_qgis.safe_interface import calculate_safe_impact

from PyQt4.QtCore import QCoreApplication, QSettings, QSize
from PyQt4.QtGui import QApplication
from qgis.core import (
    QgsApplication,
    QgsProviderRegistry,
    QgsVectorLayer,
    QgsMapLayer,
    QgsRectangle
    )


def index(request):
    layers = Layer.objects.all()
    context = {'layers': layers}
    return render(request, 'layers/index.html', context)


def detail(request, layer_slug):
    layer = get_object_or_404(Layer, slug=layer_slug)

    #get GeoJSON file
    layer_folder = os.path.join(settings.MEDIA_URL, 'layers', layer_slug)
    geometry_json = os.path.join(layer_folder, 'raw', 'geometry.json')
    context = {'layer': layer}
    context['geojson'] = geometry_json

    return render(request, 'layers/detail.html', context)


def get_layer_data(layer_name):
    layer = Layer.objects.get(name=layer_name)
    layer_path = os.path.join(settings.MEDIA_ROOT, 'layers', layer.slug, 'raw')
    os.chdir(layer_path)
    filename = glob.glob('*.shp')[0]
    layer_file = os.path.join(layer_path, filename)
    layer_object = QgsVectorLayer(layer_file, layer.name, 'ogr')
    map_layer = QgisWrapper(layer_object)

    return map_layer

@login_required(redirect_field_name='next')
def calculate(request):
    """Calculates the buildings affected by flood.
    """

    QCoreApplication.setOrganizationName('QGIS')
    QCoreApplication.setOrganizationDomain('qgis.org')
    QCoreApplication.setApplicationName('QGIS2InaSAFETesting')

    #noinspection PyPep8Naming
    gui_flag = False
    qgis_app = QgsApplication([], gui_flag)

    # Make sure QGIS_PREFIX_PATH is set in your env if needed!
    qgis_app.initQgis()


    output = os.path.join(settings.MEDIA_ROOT, 'layers', 'impact.json')

    roads = get_layer_data('Roads')
    flood = get_layer_data('Flood')

    impact_function = FloodVectorRoadsExperimentalFunction

    xmin, ymin, xmax, ymax = 121, 14.54, 121.05, 14.56

    impact_file = calculate_safe_impact(
                layers=[roads, flood],
                function=impact_function,
                extent=[xmin, ymin, xmax, ymax],
                check_integrity=False)

    os.remove(impact_geojson)

    call(['ogr2ogr', '-f', 'GeoJSON',
          output, impact_file.filename])

    impact_geojson = os.path.join(settings.MEDIA_URL, 'layers', 'impact.json')
    os.remove(impact_geojson)

    context = impact_file.keywords
    context = {}
    context['geojson'] = impact_geojson
    context['user'] = request.user

    return render(request, 'layers/calculate.html', context)
