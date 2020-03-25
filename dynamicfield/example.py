from django.db import models
from django.contrib import admin
from dynamicfield.models import DynamicField
from dynamicfield.forms import DynamicModelForm
from dynamicfield.admin import DynamicWidget


class MyModel(models.Model):
    INPUT_TYPE_CHOICES = (
        ('Char', 'Text Field (single line)'),
        ('Email', 'Email Field'),
        ('File', 'File Field'),
        ('Image', 'Image Field'),
        ('URL', 'URL Field'),
        ('Text', 'Multiline Text Area'),
    )
    fieldtype = models.CharField(choices=INPUT_TYPE_CHOICES, max_length=10, default='Char')
    value = DynamicField(blank=True, null=True)


class MyModelInline(admin.TabularInline):
    model = MyModel
    form = DynamicModelForm
    formfield_overrides = {
        DynamicField: {'widget': DynamicWidget()},
    }
