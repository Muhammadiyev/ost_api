from rest_framework import serializers
from .models import UploadedFile
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize= value.size
    if filesize > 1048576000:
        raise ValidationError("The maximum file size that can be uploaded is 1GB")
    else:
        return value

class UploadedFileSerializer(serializers.ModelSerializer):

    #file = serializers.FileField(validators=[validate_file_size])
    class Meta:
        model = UploadedFile
        fields = ['id', 'symbol',
                  'file', 'user', 'company', 'type']
