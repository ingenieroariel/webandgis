from django.core.files.storage import FileSystemStorage
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.template.defaultfilters import slugify
import zipfile
import os, errno
import glob

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class Layer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(editable=False)
    bbox = models.CharField(max_length=255, null=True, blank=True)
    original = models.FileField(storage=OverwriteStorage(),
                                upload_to='uploads', null=True, blank=True,
                                help_text="""Zip file with either geotiff and
                                        projection or shapefiles and friends""")
    style = models.TextField(null=True, blank=True)
    # type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.name)
        super(Layer, self).save(force_insert, force_update)

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

@receiver(models.signals.pre_save, sender=Layer)
def layer_handler(sender, instance, *args, **kwargs):
    """
    Post process the uploaded layer
    Get the bounding box information and save it with the model
    """

    instance.slug = slugify(instance.name)

    # Make a folder with the slug name
    # and create a 'raw' subdirectory to hold the files
    layer_folder = os.path.join(settings.MEDIA_ROOT, 'layers', instance.slug)
    create_folder(layer_folder)
    zip_out = os.path.join(layer_folder, 'raw')
    create_folder(zip_out)

    # Iterate over the files in the zip and create them in the raw folder.
    z = zipfile.ZipFile(instance.original)
    for name in z.namelist():
        outfile = open(os.path.join(zip_out, name), 'wb')
        outfile.write(z.read(name))
        outfile.close()

    # Check if it is vector or raster
    # if it has a .shp file, it is vector :)
    os.chdir(zip_out)
    shapefiles = glob.glob('*.shp')

    if len(shapefiles) > 0:
        # this means it is a vector

        # FIXME(This is a very weak way to get the shapefile)
        shapefile = shapefiles[0]

        # Use ogr to inspect the file and get the bounding box
        ds = DataSource(shapefile)
        layer = ds[0]
        extent = layer.extent.tuple
        instance.bbox = ",".join(["%s" % x for x in extent])

    # Render the tiles (if possible)