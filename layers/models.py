from django.db import models

class Layer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    original = models.FileField(upload_to='uploads', null=True, blank=True, help_text='Zip file with either geotiff and projection or shapefiles and friends')
