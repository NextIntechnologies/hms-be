from django.contrib import admin

from .models import UserTwo, Patient, Report, Doctor, Appointment, Staff, Inventry, Bed, Billing


# Register your models here
admin.site.register(UserTwo)
admin.site.register(Patient)
admin.site.register(Report)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Staff)
admin.site.register(Inventry)
admin.site.register(Bed)
admin.site.register(Billing)