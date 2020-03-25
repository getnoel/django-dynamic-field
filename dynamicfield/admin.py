from PIL import Image, UnidentifiedImageError
from django.db import models
from django.conf import settings
from django.forms import MultiWidget, Textarea
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget


class DynamicWidget(MultiWidget):

    def __init__(self):
        return super().__init__(widgets=[Textarea, AdminFileWidget])

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        try:
            Image.open(value)
        except AttributeError:
            html = ''
        except FileNotFoundError:
            return Textarea(attrs={'cols': 80, 'rows': 1}).render(name, value)
        except UnidentifiedImageError:
            html = u'<a href="{0}{1}" target="_blank">{1}</a>'
        else:
            html = u'<a href="{0}{1}" target="_blank"><img src="{0}{1}" alt="{1}" height="150"  style="object-fit: cover;"/></a>'  # noqa: E501
        output.append(html.format(settings.MEDIA_URL, value))
        output.append(AdminFileWidget().render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))

    def decompress(self, value):
        if isinstance(value, models.fields.files.FieldFile):
            return (None, value)
        else:
            return (value, None)

    def value_from_datadict(self, data, files, name):
        try:
            return files[name]
        except KeyError:
            return data[name]
