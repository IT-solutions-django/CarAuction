from django import forms


class CarFilterForm(forms.Form):
    def __init__(self, *args, dynamic_fields=None, **kwargs):
        super().__init__(*args, **kwargs)

        if dynamic_fields:
            for field_name, choices in dynamic_fields.items():
                self.fields[field_name] = forms.ChoiceField(
                    choices=[('', f'Выберите {field_name}')] + [(choice, choice) for choice in choices[0]],
                    required=False
                )
