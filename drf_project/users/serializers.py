from rest_framework import serializers
from .models import UM


class UMSerializer(serializers.ModelSerializer):
    class Meta:
        model = UM
        fields = ('id', 'username')