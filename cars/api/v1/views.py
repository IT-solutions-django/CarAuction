from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from cars.models import Car
from django.db.models import Count
from cars.api.v1.serializers import CarPrivodSerializer, CarKPPSerializer, CarModelSerializer


class ListPrivodView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Car.objects.values('priv_id__name').annotate(count=Count('priv_id'))
        serializer = CarPrivodSerializer(queryset, many=True)
        return Response(serializer.data)


class ListKPPView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Car.objects.values('kpp_type__name').annotate(count=Count('kpp_type'))
        serializer = CarKPPSerializer(queryset, many=True)
        return Response(serializer.data)


class ListColorView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        all_colors = Car.objects.values('true_color', 'color_id__name').distinct()

        color_map = {}
        for color in all_colors:
            true_color = color['true_color']
            car_color = color['color_id__name']

            if true_color not in color_map:
                color_map[true_color] = set()
            color_map[true_color].add(car_color)

        result = [{'main_color': true_color, 'car_colors': list(colors)} for true_color, colors in color_map.items()]

        return Response(result)


class ListModelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Car.objects.values('model_id__name').annotate(count=Count('model_id'))
        serializer = CarModelSerializer(queryset, many=True)
        return Response(serializer.data)
