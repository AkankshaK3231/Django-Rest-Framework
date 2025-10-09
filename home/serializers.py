from rest_framework import serializers
from .models import Person, Color

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']


class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    class Meta :
        model = Person
        fields = '__all__'
        

    def validate(self,data):

        special_characters = "!@#$%^&*()_+-=<>,/"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('name cannot contain special chars')

        if data['age']<18:
            raise serializers.ValidationError('age should be greater than 18')
        return data