from rest_framework import serializers
from .models import UploadedFile



class UploadedFileSerializer(serializers.ModelSerializer):
    # children = DRecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = UploadedFile
        fields = ['id', 'symbol',
                  'file', 'user', 'company','type']

