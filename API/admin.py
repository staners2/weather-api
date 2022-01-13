from django.contrib import admin
from .models import Language, Cities, UserProfile

admin.site.register(Language)
admin.site.register(Cities)
admin.site.register(UserProfile)

# Register your models here.
