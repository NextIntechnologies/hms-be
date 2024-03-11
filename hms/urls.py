from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='index'),
    path('login', views.login, name='index'),
    path('patients', views.patient, name='index'),
    path('patients/<str:id>', views.patient, name='index'),
    path('labs', views.lab, name='index'),
    path('doctors', views.doctor, name='index'),
    path('appointments', views.appointment, name='index'),
    path('staffs', views.staff, name='index'),
    path('inventries', views.inventry, name='index'),
    path('beds', views.bed, name='index'),
    path('forget-password', views.forget_password, name='index'),
    path('billings', views.billing, name='index'),
    path('patient-login', views.patient_login, name='index'),
    path('patient-register', views.patient_register, name='index'),
    path('activities', views.activity, name='index'),
    path('categories', views.patientCategory, name='index'),
    path('patient-records/<str:id>', views.patientRecords, name='index'),
     path('labs/<str:id>', views.lab, name='index')
]