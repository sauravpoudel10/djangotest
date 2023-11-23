from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.utils import timezone



class Blog(models.Model):
    image = models.ImageField( default = None, upload_to ='blogpic')
    title = models.CharField(max_length =100)
    header =  models.CharField(max_length =300 )
    content = models.TextField()
    author = models.ForeignKey(User , on_delete= models.CASCADE)
    dateposted = models.DateTimeField(default=timezone.now)
    keyword = models.CharField(max_length =250)
    keyword_content =  models.TextField()


    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse ('blogdetail', kwargs={'pk' :self.pk})
    
    def user_blogs(self):
        return Blog.objects.filter(author=self)

    def save(self,*args ,**kwargs):
        super().save(*args ,**kwargs)

        img = Image.open(self.image.path)

        if img.height>1000 or img.width > 900:
            output_size = (900,700)
            img.thumbnail(output_size)
            img.save(self.image.path)

        
class UploadedImage(models.Model):
    original_image = models.ImageField(upload_to='uploads/')
    enhanced_image = models.ImageField(upload_to='enhanced/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"




class UploadedAudio(models.Model):
    audio = models.FileField(upload_to='uploaded_audios/')

# class EnhancedImage(models.Model):
#     original_image = models.ImageField(upload_to='images/')
#     enhanced_image = models.ImageField(blank=True, null=True, upload_to='enhanced_images/')

#     def __str__(self):
#         return f"Enhanced Image {self.id}"






class Video(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
class VideoClip(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    clip = models.FileField(upload_to='clips/')
    start_time = models.IntegerField()  # in seconds
    end_time = models.IntegerField()  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    upload_date = models.DateTimeField(auto_now_add=True)
 
