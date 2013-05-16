from django.db import models
from django.dispatch import receiver


class Layer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    bbox = models.CharField(max_length=255, null=True, blank=True)
    original = models.FileField(upload_to='uploads', null=True, blank=True, help_text='Zip file with either geotiff and projection or shapefiles and friends')


    def __unicode__(self):
        return self.name


@receiver(models.signals.pre_save, sender=Layer)
def layer_handler(sender, instance, *args, **kwargs):
    """Post process the uploaded layer

       Get the bounding box information and save it with the model
    """
    # Unzip the file
    #import ipdb;ipdb.set_trace()
    # Check if it is vector or raster

    # Use ogr to inspect the file and get the bounding box
    instance.bbox = '0,0,0,0'

    # Render the tiles (if possible)
