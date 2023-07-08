from django.db import models
import os
def slider_image_location(instance, filename):
    upload_path=f"slider/"
    return os.path.join(upload_path, filename)
class HomePageSliderImage(models.Model):

    image = models.ImageField(
        upload_to=slider_image_location, blank=True, null=True ,)

    def __str__(self):
        return "slider image "+str(self.id)