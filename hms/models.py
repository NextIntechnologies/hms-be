from django.db import models

# Create your models here.

class UserTwo (models.Model):
    id=models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class Patient (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    dob = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

class Report (models.Model):
    id=models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
    labTest = models.CharField(max_length=200)
    report = models.FileField(upload_to='')

class Doctor (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    experience = models.IntegerField(max_length=200)
    speciality = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

class Appointment (models.Model):
    id=models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

class Staff (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


class Inventry (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    price = models.IntegerField(max_length=200)
    stock = models.IntegerField(max_length=200)
    expiryDate = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)

class Bed (models.Model):
    id=models.AutoField(primary_key=True)
    roomNumber = models.CharField(max_length=200)
    roomType = models.CharField(max_length=200)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    allotmentDate = models.CharField(max_length=200)
    dischargeDate = models.CharField(max_length=200)


class Billing (models.Model):
    id=models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.CharField(max_length=200)
    admissionDate = models.CharField(max_length=200)
    dischargeDate = models.CharField(max_length=200)
    costOfTreatment = models.IntegerField(max_length=200)
    bill = models.FileField(upload_to='')


class Otp (models.Model):
    id=models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)
    otp = models.CharField(max_length=200)
