from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from .forms import Step0Form, Step1Form, Step2Form, Step3FormSet
from .models import FormWizard, Address

FORMS = [("step0", Step0Form),
         ("step1", Step1Form),
         ("step2", Step2Form),
         ("step3", Step3FormSet)]

TEMPLATES = {"step0": "app/step0.html",
             "step1": "app/step1.html",
             "step2": "app/step2.html",
             "step3": "app/step3.html"}

MESSAGES = {
    "step0": "Bem-vindo ao Form Wizard",
    "step1": "Informações pessoais",
    "step2": "Contato",
    "step3": "Endereço"
}
#usar formset
#estudar a wizard form
class FormWizardView(SessionWizardView):
    template_name = "app/form_wizard.html"
    form_list = FORMS


    def get_template_names(self):
        return ["app/form_wizard.html"]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        step_count = len(FORMS)
        step_width = 100 / step_count if step_count > 0 else 100
        current_step = self.steps.current
        context.update({
            'step_count': step_count,
            'step_width': step_width,
            'template_name': TEMPLATES[self.steps.current],
            'step_message': MESSAGES[current_step]
        })
        return context

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
        print(form_data)

        form_data_model = FormWizard(
            name=form_data[1]['name'],
            full_name=form_data[1]['full_name'],
            birth_date=form_data[1]['birth_date'],
            phone=form_data[2]['phone'],
            email=form_data[2]['email'],
        )
        form_data_model.save()

        for address_data in form_data[3]:
            address_instance = Address(
                address=address_data['address'],
                state=address_data['state'],
                city=address_data['city'],
                country=address_data['country'],
                form_wizard=form_data_model
            )
            address_instance.save()

        return render(self.request, 'app/done.html', {
            'form_data': form_data,
        })
