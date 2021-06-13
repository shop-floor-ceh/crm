from django.contrib import admin
from main.models import Project, Date, Participant, Group

# Register your models here.
admin.site.register(Project)
admin.site.register(Date)
admin.site.register(Group)
admin.site.register(Participant)
