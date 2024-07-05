from django import forms
from .models import FormWizard

class Step1Form(forms.ModelForm):
    class Meta:
        model = FormWizard
        fields = ['name', 'full_name', 'birth_date']

    birth_date = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].label = 'Nome Completo'

class Step2Form(forms.ModelForm):
    class Meta:
        model = FormWizard
        fields = ['phone', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].label = 'Celular'
        self.fields['email'].label = 'Email'

class Step3Form(forms.ModelForm):
    class Meta:
        model = FormWizard
        fields = ['address', 'state', 'city', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].label = 'Endereço'
        self.fields['state'].label = 'Estado'
        self.fields['city'].label = 'Cidade'
        self.fields['country'].label = 'País'