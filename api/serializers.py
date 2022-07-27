from rest_framework import serializers
from main.models import Customer,Film
class CustomerSelializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
class FilmsSelializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = "__all__"