from django.urls import path
from .views import FormWizardView

app_name = "form_wizard"

urlpatterns = [
    path('', FormWizardView.as_view(), name='form_wizard'),
]
