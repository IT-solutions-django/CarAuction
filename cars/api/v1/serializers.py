from rest_framework import serializers
from cars.models import UniqueMarkModel, Car, Privod


# Serializer для ListDetailView
class CarDetailSerializer(serializers.Serializer):
    category_name = serializers.SerializerMethodField()
    count = serializers.IntegerField()

    class Meta:
        fields = ('category_name', 'count')

    def get_category_name(self, obj):
        field_name = self.context.get('field_name')
        return obj.get(f'{field_name}', '')


# Serializer для ListUniqueMarkModelView
class CarUniqueMarkModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    cars = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cars'] = representation['cars'].split(',')
        return representation


# Serializer для ListNotDetailView
class CarNotDetailSerializer(CarDetailSerializer):
    def get_category_name(self, obj):
        field_name = self.context.get('field_name')
        return obj.get(f'{field_name}__name', '')
