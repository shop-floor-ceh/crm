from django.contrib import admin
from account.models import Account, SocialNetworks, Notification

admin.site.register(Account)
admin.site.register(SocialNetworks)
admin.site.register(Notification)
