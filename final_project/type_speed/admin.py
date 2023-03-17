from django.contrib import admin

from .models import User, Scores, CustomText

admin.site.register(User)
admin.site.register(Scores)
admin.site.register(CustomText)
