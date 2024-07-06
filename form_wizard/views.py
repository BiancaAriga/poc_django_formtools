from django.shortcuts import render,redirect
from formtools.wizard.views import SessionWizardView
from .forms import Step1Form, Step2Form, Step3Form
from .models import FormWizard

FORMS = [("step1", Step1Form),
         ("step2", Step2Form),
         ("step3", Step3Form)]

class FormWizardView(SessionWizardView):
    template_name = "app/form_wizard.html"
    form_list = FORMS
    
    def render_goto_step(self, goto_step, **kwargs):
        form1 = self.get_form(self.storage.current_step, data=self.request.POST,files=self.request.FILES)
        
        if form1:
            self.storage.set_step_data(self.storage.current_step, self.process_step(form1))
            self.storage.set_step_files(self.storage.current_step, self.process_step_files(form1))

        self.storage.current_step = goto_step

        form = self.get_form(
            data=self.storage.get_step_data(self.steps.current),
            files=self.storage.get_step_files(self.steps.current))

        return self.render(form, **kwargs)
    
    def render_next_step(self, form, **kwargs):
      #  print(self.storage.get_step_data(self.steps.next))
        return super().render_next_step(form, **kwargs)


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
