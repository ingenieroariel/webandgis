from django.db import models
from django.dispatch import receiver
from django.conf import settings
import zipfile
import os, errno


class Layer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    bbox = models.CharField(max_length=255, null=True, blank=True)
    original = models.FileField(upload_to='uploads', null=True, blank=True, help_text='Zip file with either geotiff and projection or shapefiles and friends')


    def __unicode__(self):
        return self.name

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

@receiver(models.signals.pre_save, sender=Layer)
def layer_handler(sender, instance, *args, **kwargs):
    """Post process the uploaded layer

       Get the bounding box information and save it with the model
    """
    zip_path = instance.original.path
 

    # Make a folder with the slug name
    # and create a 'raw' subdirectory to hold the files
    layer_folder = os.path.join(settings.MEDIA_ROOT, 'layers', instance.slug)
    create_folder(layer_folder)
    zip_out = os.path.join(layer_folder, 'raw')
    create_folder(zip_out)

    # Iterate over the files in the zip and create them in the raw folder.
    fh = open(zip_path, 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():
        outfile = open(os.path.join(zip_out, name), 'wb')
        outfile.write(z.read(name))
        outfile.close()
    fh.close()
 
    # Check if it is vector or raster

    # Use ogr to inspect the file and get the bounding box
    instance.bbox = '0,0,0,0'

    # Render the tiles (if possible)
