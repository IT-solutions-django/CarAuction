from django.core.exceptions import FieldError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from cars.models import Car, UniqueMarkModel, UniqueCarColor
from django.db.models import Count
from cars.api.v1.serializers import CarDetailSerializer, CarUniqueMarkModelSerializer, CarNotDetailSerializer


# Вьюха для получения данных о кол-ве автомобилей с определенными параметрами (field_name)
class ListDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, field_name):
        try:
            queryset = Car.objects.values(f'{field_name}__name').annotate(count=Count(f'{field_name}'))
            serializer = CarDetailSerializer(queryset, many=True, context={'field_name': f'{field_name}__name'})
        except FieldError:
            queryset = Car.objects.values(f'{field_name}').annotate(count=Count(f'{field_name}'))
            serializer = CarDetailSerializer(queryset, many=True, context={'field_name': field_name})
        return Response(serializer.data)


# Вьюха для получения данных в виде: {Обобщенное название цвета: Список соответствующих цветов}
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


# Вьюха для получения списка машин по фильтрации
class ListUniqueMarkModelView(APIView):
    permission_classes = [AllowAny]

    model_serializer_map = {
        'mark': UniqueMarkModel,
        'color': UniqueCarColor
    }

    def get(self, request):
        field_filter = request.GET
        combined_results = []

        for field_name, value in field_filter.items():
            if not value:
                continue
            model_class = self.model_serializer_map.get(field_name)
            queryset = model_class.objects.filter(name=value)
            combined_results.extend(queryset)

        combined_results = list(set(combined_results))

        serializer = CarUniqueMarkModelSerializer(combined_results, many=True)
        return Response(serializer.data)


# Вьюха для получения данных о кол-ве авто,
# которые имееют определенные параметры (field_name), но этим параметрам (field_name)
# не сопоставлено обобщенное название (true_...)
class ListNotDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, field_name):
        if field_name == 'priv_id':
            queryset = Car.objects.filter(true_priv='').values(f'{field_name}__name').annotate(
                count=Count(f'{field_name}')
            )
        elif field_name == 'kpp_type':
            queryset = Car.objects.filter(true_kpp='').values(f'{field_name}__name').annotate(
                count=Count(f'{field_name}')
            )
        elif field_name == 'color_id':
            queryset = Car.objects.filter(true_color='').values(f'{field_name}__name').annotate(
                count=Count(f'{field_name}')
            )
        else:
            return Response({'detail': 'Для данного поля нет данных'})
        serializer = CarNotDetailSerializer(queryset, many=True, context={'field_name': field_name})
        return Response(serializer.data)
