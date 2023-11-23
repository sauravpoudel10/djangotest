import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from .models import UploadedImage, UploadedAudio, EnhancedImage , VideoClip


class Command(BaseCommand):
    help = 'Deletes uploaded media files older than a specified duration'

    def handle(self, *args, **options):
        duration = datetime.timedelta(hours=1)  # Define the duration (1 hour in this case)
        now = datetime.datetime.now()

        # Delete uploaded images older than the specified duration
        old_images = UploadedImage.objects.filter(uploaded_at__lt=now - duration)
        for img in old_images:
            img.original_image.delete(save=False)
            img.enhanced_image.delete(save=False)
            img.delete()

        # Delete uploaded audios older than the specified duration
        old_audios = UploadedAudio.objects.filter(upload_at__lt=now - duration)
        for audio in old_audios:
            audio.audio.delete(save=False)
            audio.delete()

        # Delete enhanced images older than the specified duration
        old_enhanced_images = EnhancedImage.objects.filter(upload_at__lt=now - duration)
        for enhanced_img in old_enhanced_images:
            enhanced_img.original_image.delete(save=False)
            enhanced_img.enhanced_image.delete(save=False)
            enhanced_img.delete()

        old_video_clips = VideoClip.objects.filter(upload_date__lt=now - duration)
        for video_clip in old_video_clips:
            video_clip.clip.delete(save=False)
            video_clip.delete()