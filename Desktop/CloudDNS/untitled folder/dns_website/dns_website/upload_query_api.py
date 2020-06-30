from rest_framework import serializers
from .models import UploadQuery
from rest_framework import viewsets

class UploadQuerySerialiser(serializers.Serializer):
    path = serializers.CharField(max_length=200)

class UploadViewSet(viewsets.ModelViewSet):
	queryset = UploadQuery.objects.all()
	serializer_class = UploadQuerySerialiser
