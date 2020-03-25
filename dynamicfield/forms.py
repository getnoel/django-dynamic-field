from django.forms import ModelForm


class DynamicModelForm(ModelForm):

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if self.files.get(self.prefix + '-value'):
            cleaned_data['value'] = self.files.get(self.prefix + '-value')
        return cleaned_data
