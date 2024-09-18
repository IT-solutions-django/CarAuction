from django import forms
from cars.cars_settings import CarYearEnum


class CarFilterForm(forms.Form):
    def __init__(self, *args, dynamic_fields=None, **kwargs):
        super().__init__(*args, **kwargs)

        if dynamic_fields:
            for field_name, choices in dynamic_fields.items():
                self.fields[field_name] = forms.ChoiceField(
                    choices=[('', f'Выберите {field_name}')] + [(choice, choice) for choice in choices[0]],
                    required=False
                )

    year_from = forms.ChoiceField(
        choices=[('', 'Выберите год от')] + [(year, year) for year in CarYearEnum.year_range()],
        required=False
    )
    year_to = forms.ChoiceField(
        choices=[('', 'Выберите год до')] + [(year, year) for year in CarYearEnum.year_range()],
        required=False)
