import ast
from django.db import models
from django.forms.models import model_to_dict


class BorrowerDataBlueprint(models.Model):
    charfield = models.CharField(blank=True, null=True, max_length=50)
    emailfield = models.EmailField(blank=True, null=True)
    filefield = models.FileField(blank=True, null=True, upload_to='uploads/')
    imagefield = models.ImageField(blank=True, null=True, upload_to='uploads/')
    urlfield = models.URLField(blank=True, null=True)
    textfield = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class DynamicField(models.TextField):

    def from_db_value(self, value, expression, connection):
        try:
            value = dict(ast.literal_eval(str(value)))
        except (SyntaxError, ValueError, TypeError):
            value = {'charfield': value}
        bb = BorrowerDataBlueprint(**value)
        return (
                bb.charfield
                or bb.emailfield
                or bb.filefield
                or bb.imagefield
                or bb.urlfield
                or bb.textfield
            )

    def pre_save(self, model_instance, add):
        if add or model_instance.value is None:
            return
        sent_value = model_instance.value
        fieldtype = getattr(model_instance, 'fieldtype', 'charfield').lower()
        fieldname = '{}field'.format(fieldtype)
        if model_instance.value == '':
            model_instance.refresh_from_db(fields=['value'])
        bb = BorrowerDataBlueprint(**{fieldname: model_instance.value})
        field = getattr(bb, fieldname)
        if hasattr(field, 'name'):
            if sent_value:
                field.save(field.name, model_instance.value, save=False)
            return {fieldname: field.name}
        else:
            return model_to_dict(bb, fields=[fieldname])

    def to_python(self, value):
        if isinstance(value, dict):
            return super().to_python(value)
        return value
