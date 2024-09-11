from rest_framework import serializers


class CarPrivodSerializer(serializers.Serializer):
    privod_name = serializers.CharField(source='priv_id__name')
    count = serializers.IntegerField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        fields = ('privod_name', 'count', 'category_name')

    def get_category_name(self, obj):

        privod_name = obj.get('priv_id__name', '')

        if privod_name == 'FF':
            return 'Передний привод'

        elif privod_name == 'FR':
            return 'Задний привод'

        return 'Полный привод'


class CarKPPSerializer(serializers.Serializer):
    kpp_type = serializers.CharField(source='kpp_type__name')
    count = serializers.IntegerField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        fields = ('kpp_type', 'count', 'category_name')

    def get_category_name(self, obj):
        kpp_name = obj.get('kpp_type__name', '')

        if kpp_name.isalpha():
            return 'Автоматическая'

        return 'Механическая'


class CarModelSerializer(serializers.Serializer):
    model_name = serializers.CharField(source='model_id__name')
    count = serializers.IntegerField()

    class Meta:
        fields = ('model_name', 'count')
