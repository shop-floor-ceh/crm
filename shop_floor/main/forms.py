from django.forms import ModelForm
from main.models import Project


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'synopsis',
            'literary_script',
            'directors_script',
            'kpp',
            'open_to_join',
            'ended',
            'about_project',
            'admin',
        ]
