from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from .forms import Step1Form, Step2Form, Step3Form
from .models import FormWizard

FORMS = [("step1", Step1Form),
         ("step2", Step2Form),
         ("step3", Step3Form)]

TEMPLATES = {"step1": "app/step1.html",
             "step2": "app/step2.html",
             "step3": "app/step3.html"}

class FormWizardView(SessionWizardView):
    template_name = "app/form_wizard.html"
    form_list = FORMS

    ##def get_template_names(self):
        #return [TEMPLATES[self.steps.current]]
        

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]

        form_data_model = FormWizard(
            name=form_data[0]['name'],
            full_name=form_data[0]['full_name'],
            birth_date=form_data[0]['birth_date'],
            phone=form_data[1]['phone'],
            email=form_data[1]['email'],
            address=form_data[2]['address'],
            state=form_data[2]['state'],
            city=form_data[2]['city'],
            country=form_data[2]['country'],
        )
        form_data_model.save()

        return render(self.request, 'app/done.html', {
            'form_data': form_data,
        })
