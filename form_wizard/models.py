from django.db import models

class FormWizard(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Address(models.Model):
    form_wizard = models.ForeignKey(FormWizard, related_name='addresses', on_delete=models.CASCADE)
    address = models.TextField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}"
