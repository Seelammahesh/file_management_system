# api/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

#Validate file extension
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower().replace('.', '')
    allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
    if ext not in allowed_extensions:
        raise ValidationError(
            f'Unsupported file extension. Allowed: {", ".join(allowed_extensions)}'
        )

#Generate file path for user uploads
def user_directory_path(instance, filename):
    return f'files/user_{instance.owner.id}/folder_{instance.folder.id}/{filename}'


#Folder Model For Organizing Files
class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'owner')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.owner.username}"


#File Model For Storing Uploaded Files
class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path,validators=[validate_file_extension])
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file_size = models.IntegerField(default=0)  # in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    #Get file extension
    def get_file_extension(self):
        return os.path.splitext(self.file.name)[1].lower()