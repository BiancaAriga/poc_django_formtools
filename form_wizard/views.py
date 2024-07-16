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

ADDRESS_COUNT = 2

class FormWizardView(SessionWizardView):
    template_name = "app/form_wizard.html"
    form_list = FORMS
    _add_desktop_to_prefix = False

    def get_template_names(self):
        return ["app/form_wizard.html"]
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        step_count = len(FORMS)
        step_width = 100 / step_count if step_count > 0 else 100
        current_step = self.steps.current

        self._add_desktop_to_prefix = True
        context.update({
            'step_count': step_count,
            'step_width': step_width,
            'template_name': TEMPLATES[self.steps.current],
            'step_message': MESSAGES[current_step],
            'template_names': [TEMPLATES[step] for step in self.steps.all],
            'all_forms': [self.get_form(step) for step in self.form_list]
        })
        self._add_desktop_to_prefix = False
        if current_step == 'step3':
            context['number_of_address'] = list(range(ADDRESS_COUNT))

        return context

    def get_form_prefix(self, step=None, form=None):
        if self._add_desktop_to_prefix:
            return 'desktop_' + super().get_form_prefix(step, form)
        else:
            return super().get_form_prefix(step, form)

    def render_goto_step(self, goto_step, **kwargs):
        form1 = self.get_form(self.storage.current_step, data=self.request.POST, files=self.request.FILES)
        print(form1)

        if form1:
            self.storage.set_step_data(self.storage.current_step, self.process_step(form1))
            self.storage.set_step_files(self.storage.current_step, self.process_step_files(form1))

        self.storage.current_step = goto_step

        form = self.get_form(
            data=self.storage.get_step_data(self.steps.current),
            files=self.storage.get_step_files(self.steps.current))

        return self.render(form, **kwargs)
    
    def post(self, *args, **kwargs):
        print(self.request.POST)
        form_wizard_override = self.request.POST.get('wizard-desktop-override', None)
        if form_wizard_override:
            self._add_desktop_to_prefix = True
            self.storage.current_step = self.steps.last
            invalid = False
            for step in self.form_list:
                form = self.get_form(step, data=self.request.POST, files=self.request.FILES)
                print(form)
                if not form.is_valid():
                    print(f'{step} invalid:', form.errors)
                    invalid = True
                else:
                    print(f'{step} valid:', form.cleaned_data)
                    self.storage.set_step_data(step, self.process_step(form))
                    self.storage.set_step_files(step, self.process_step_files(form))
            if invalid:
                print('invalid desktop form')
                next_render = self.render(form)
            print("calling done!")
            next_render = self.render_done(form, **kwargs)
            self._add_desktop_to_prefix = False
            return next_render


        return super().post(*args, **kwargs)

    def done(self, form_list, **kwargs):
        print('passou em done')
        form_data = [form.cleaned_data for form in form_list]

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
