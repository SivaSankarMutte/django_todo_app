from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from App1.models import Faculty


# Register your models here.

@admin.register(Faculty)
class ViewAdmin(ImportExportModelAdmin):
	pass
