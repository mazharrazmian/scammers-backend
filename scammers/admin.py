from django.contrib import admin
from . import models
# Register your models here.

class ImageAdminInline(admin.TabularInline):
    model = models.Images

class ScammerAdmin(admin.ModelAdmin):
    inlines = (ImageAdminInline, )
admin.site.register(models.Scammer, ScammerAdmin)

admin.site.register(models.User)