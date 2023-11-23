
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password1' ,'password2']



class imguploadform(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title'  ,'header','content' ,  'image' ,'keyword','keyword_content']



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'url']




class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['original_image']






class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedAudio
        fields = ['audio']



# class ImageEnhancementForm(forms.ModelForm):
#     class Meta:
#         model = EnhancedImage
#         fields = ['original_image']