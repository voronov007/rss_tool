from django.contrib.auth.models import User
from rest_framework import serializers


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    # feeds = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('email', )
