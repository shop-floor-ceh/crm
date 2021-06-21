from django.forms import ModelForm
from main.models import Project, Participant, Date


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


class CreateParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = [
            'participant',
            'name',
            'can_change_main_information',
            'can_add_participant',
            'can_change_synopsis',
            'can_change_literary_script',
            'can_change_directors_scripts',
            'can_change_kpp',
            'can_add_dates'
        ]


class CreateDateForProjectForm(ModelForm):
    class Meta:
        model = Date
        fields = [
            'visiting_date',
            'visiting_time',
            'address',
            'setting',
            'scene'
        ]
