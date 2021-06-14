from django.forms import ModelForm
from main.models import Project
from account.models import Account


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

    # def __init__(self, admin_username, *args, **kwargs):
    #     super(CreateProjectForm, self).__init__(*args, **kwargs)
    #     self.fields['admin'] = Account.objects.get(username=admin_username)
