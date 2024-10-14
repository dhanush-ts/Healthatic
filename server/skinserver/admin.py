from django.contrib import admin
from skinserver.models import User, Hospital, History

admin.site.register(User)
admin.site.register(Hospital)
admin.site.register(History)