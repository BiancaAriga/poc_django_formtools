from django import forms
from django.forms import inlineformset_factory
from .models import FormWizard, Address
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class Step0Form(forms.Form):
    pass

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
        self.fields['name'].label = 'Nome'
        self.fields['full_name'].label = 'Nome Completo'
        self.helper = FormHelper()
        self.helper.label_class = "form-label position-absolute start-5 m-0 py-3 px-2"
        self.helper.layout = Layout(
            Field(
                'name', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
            Field(
                'full_name', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
            Field(
                'birth_date', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
        )



class Step2Form(forms.ModelForm):
    class Meta:
        model = FormWizard
        fields = ['phone', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].label = 'Celular'
        self.fields['email'].label = 'Email'
        self.helper = FormHelper()
        self.helper.label_class = "form-label position-absolute start-5 m-0 py-3 px-2"
        self.helper.layout = Layout(
            Field('phone', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
            Field('email', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
        )

class Step3Form(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'state', 'city', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].label = 'Endereço'
        self.fields['state'].label = 'Estado'
        self.fields['city'].label = 'Cidade'
        self.fields['country'].label = 'País'
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = "form-label position-absolute start-5 m-0 py-3 px-2"
        self.helper.layout = Layout(
            Field('address', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3 address', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
            Field('state', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
            Field('city', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
            Field('country', template='app/custom_field.html',
                css_class='form-control rounded-3 p-3', 
                wrapper_class='pattern-form-floating position-relative mb-4',
            ),
        )

Step3FormSet = inlineformset_factory(FormWizard, Address, form=Step3Form, can_delete=False, extra=2)

