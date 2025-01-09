from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# Create your models here.
class Watches(models.Model):
    id=models.IntegerField
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=30)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def get_image_path(self):
        if self.image:
            return self.image.path
        return ""
    
    # def save(self, *args, **kwargs):
    #     old_data = Watches.objects.get(id=self.id)
    #     if old_data.image != self.image:
    #         old_data.image.delete(save=False)
    #     super(Watches, self).save(*args, **kwargs)



    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            rates = [rating.rating for rating in ratings]
            average = round(sum(rates)/len(rates),2)
            return average
        return 0

@receiver(post_delete, sender=Watches)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.get_image_path() 
            
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted image file at {image_path}")
        else:
            print(f"Image file at {image_path} does not exist.")
                
from django.contrib.auth.models import User
class RatingComment(models.Model):
    product = models.ForeignKey(Watches, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    print(" product details",product, user, rating, comment, created_on)
    