from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserTwo, Patient, Report, Doctor, Appointment, Staff, Inventry, Bed, Billing
import json
from django.http import QueryDict
from django.core.mail import send_mail
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from django.utils import timezone

def generate_bill(customer_name, items, total_amount, output_file):
    # Create PDF document
    c = canvas.Canvas("media/"+output_file, pagesize=letter)
    
    # Set font and size
    c.setFont("Helvetica", 12)

    # Add content to the PDF
    c.drawString(100, 750, "Invoice")
    c.drawString(100, 730, "Patient Name: {}".format(customer_name))
    c.drawString(100, 710, "Admission Date: {}".format(items[0]))
    c.drawString(100, 690, "Discharge Date: {}".format(items[1]))


    # Display total amount
    c.drawString(100, 690 - 20, "Total Amount: Rs {:.2f}".format(total_amount))

    # Save the PDF
    c.save()
# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        user = UserTwo.objects.filter(email=request_data['email'])
        if user:
            return JsonResponse({ 'message': 'User already exists'}, status=400)
        user = UserTwo(
            password = request_data['password'],
            email = request_data['email'],
        )
        user.save()
        return JsonResponse({'message': 'Registered successfully'}, status=200)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        user = UserTwo.objects.filter(email=request_data['email'])
        if not user:
            return JsonResponse({ 'message': 'User does not exist'}, status=400)
        if user[0].password != request_data['password']:
            return JsonResponse({ 'message': 'Incorrect password'}, status=400)
        return JsonResponse({'message': 'Logged in successfully'}, status=200)

@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
    
        request_data = json.loads(request.body.decode('utf-8'))
        if request_data['action']=='sendOtp':

            user = UserTwo.objects.filter(email=request_data['email'])
            if not user:
                return JsonResponse({ 'message': 'User does not exist'}, status=400)
            
            send_mail(
                subject='Otp for password reset',
                message='Your otp is 1234',
                recipient_list=[request_data['email']],
                from_email='<from-email>'
            )
            return JsonResponse({'message': 'Password sent to email'}, status=200)
        if request_data['action']=='verifyOtp':
            return JsonResponse({'message': 'Otp verified successfully'}, status=200)
        
        user = UserTwo.objects.filter(email=request_data['email'])
        if not user:
            return JsonResponse({ 'message': 'User does not exist'}, status=400)
        user = user[0]
        user.password = request_data['password']
        user.save()
        return JsonResponse({'message': 'Password updated successfully'}, status=200)


@csrf_exempt
def patient(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        patient = Patient(
            name = request_data['name'],
            department = request_data['department'],
            dob = request_data['dob'],
            gender = request_data['gender'],
            email = request_data['email'],
            phone = request_data['phone'],
        )
        patient.save()
        return JsonResponse({'message': 'Patient added successfully'}, status=200)
    if request.method == 'GET':
        patients = Patient.objects.all()
        response = []
        for patient in patients:
            response.append({
                'id': patient.id,
                'name': patient.name,
                'department': patient.department,
                'dob': patient.dob,
                'gender': patient.gender,
                'email': patient.email,
                'phone': patient.phone,
            })
        return JsonResponse({'patients': response}, status=200)
    if request.method == 'PUT':
        request_data = json.loads(request.body.decode('utf-8'))
        patient = Patient.objects.filter(id=request_data['id'])
        if not patient:
            return JsonResponse({ 'message': 'Patient does not exist'}, status=400)
        patient = patient[0]
        patient.name = request_data['name']
        patient.department = request_data['department']
        patient.dob = request_data['dob']
        patient.gender = request_data['gender']
        patient.email = request_data['email']
        patient.phone = request_data['phone']
        patient.save()
        return JsonResponse({'message': 'Patient updated successfully'}, status=200)
    if request.method == 'DELETE':
        request_data = json.loads(request.body.decode('utf-8'))
        patient = Patient.objects.filter(id=request_data['id'])
        if not patient:
            return JsonResponse({ 'message': 'Patient does not exist'}, status=400)
        patient.delete()
        return JsonResponse({'message': 'Patient deleted successfully'}, status=200)

@csrf_exempt
def lab(request, id=None):
    if request.method == 'POST':
        if request.POST.get('update'):
            lab = Report.objects.filter(id=request.POST.get('id'))
            if not lab:
                return JsonResponse({ 'message': 'Lab does not exist'}, status=400)
            lab = lab[0]
            lab.patient = Patient.objects.get(id=request.POST.get('patient'))
            lab.date = request.POST.get('date')
            lab.labTest = request.POST.get('labTest')
            lab.report = request.FILES['report']
            lab.save()
            
            return JsonResponse({'message': 'Lab updated successfully'}, status=200)
        patient = Patient.objects.filter(id=request.POST.get('patient'))
        report = Report(
            patient = Patient.objects.get(id=request.POST.get('patient')),
            date = request.POST.get('date'),
            labTest = request.POST.get('labTest'),
            report = request.FILES['report']
        )
        report.save()
        send_mail(
            subject='Lab Report',
            message='Your lab report is ready. Please find the attachment ',
            recipient_list=[patient[0].email],
            from_email='<from-email>')
        return JsonResponse({'message': 'Lab added successfully'}, status=200)

    if request.method == 'GET':
        reports = Report.objects.all()
        response = []
        for report in reports:
            response.append({
                'id': report.id,
                'patient': {'name':report.patient.name,'id': report.patient.id},
                'date': report.date,
                'labTest': report.labTest,
                'report': report.report.url,
            })
        return JsonResponse({'reports': response}, status=200)


    if request.method == 'DELETE':
        report = Report.objects.filter(id=id)
        if not report:
            return JsonResponse({ 'message': 'Report does not exist'}, status=400)
        report.delete()
        return JsonResponse({'message': 'Report deleted successfully'}, status=200)

@csrf_exempt
def doctor(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        doctor = Doctor(
            name = request_data['name'],
            experience = request_data['experience'],
            speciality = request_data['speciality'],
            gender = request_data['gender'],
            email = request_data['email'],
            phone = request_data['phone'],
        )
        doctor.save()
        return JsonResponse({'message': 'Doctor added successfully'}, status=200)

    if request.method == 'GET':
        doctors = Doctor.objects.all()
        response = []
        for doctor in doctors:
            response.append({
                'id': doctor.id,
                'name': doctor.name,
                'experience': doctor.experience,
                'speciality': doctor.speciality,
                'gender': doctor.gender,
                'email': doctor.email,
                'phone': doctor.phone,
            })
        return JsonResponse({'doctors': response}, status=200)

    if request.method == 'PUT':
        request_data = json.loads(request.body.decode('utf-8'))
        doctor = Doctor.objects.filter(id=request_data['id'])
        if not doctor:
            return JsonResponse({ 'message': 'Doctor does not exist'}, status=400)
        doctor = doctor[0]
        doctor.name = request_data['name']
        doctor.experience = request_data['experience']
        doctor.speciality = request_data['speciality']
        doctor.gender = request_data['gender']
        doctor.email = request_data['email']
        doctor.phone = request_data['phone']
        doctor.save()

        return JsonResponse({'message': 'Doctor updated successfully'}, status=200)

    if request.method == 'DELETE':
        request_data = json.loads(request.body.decode('utf-8'))
        doctor = Doctor.objects.filter(id=request_data['id'])
        if not doctor:
            return JsonResponse({ 'message': 'Doctor does not exist'}, status=400)
        doctor.delete()
        return JsonResponse({'message': 'Doctor deleted successfully'}, status=200)


@csrf_exempt
def appointment(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        appointment = Appointment(
            doctor = Doctor.objects.get(id=request_data['doctor']),
            patient = Patient.objects.get(id=request_data['patient']),
            date = request_data['date'],
            time = request_data['time'],
            status = request_data['status'],
        )
        appointment.save()
        send_mail(
            subject='Appointment Confirmation',
            message='Your appointment is confirmed with Dr. '+appointment.doctor.name+' on '+appointment.date+' at '+appointment.time,
            recipient_list=[appointment.patient.email],
            from_email='<from-email>'
        )
        return JsonResponse({'message': 'Appointment added successfully'}, status=200)

    if request.method == 'GET':
        appointments = Appointment.objects.all()
        response = []
        for appointment in appointments:
            response.append({
                'id': appointment.id,
                'doctor': {'name':appointment.doctor.name,'id': appointment.doctor.id},
                'patient': {'name':appointment.patient.name, 'id': appointment.patient.id},
                'date': appointment.date,
                'time': appointment.time,
                'status': appointment.status,
            })
        return JsonResponse({'appointments': response}, status=200)

    if request.method == 'PUT':
        request_data = json.loads(request.body.decode('utf-8'))
        appointment = Appointment.objects.filter(id=request_data['id'])
        if not appointment:
            return JsonResponse({ 'message': 'Appointment does not exist'}, status=400)
        appointment = appointment[0]
        appointment.doctor = Doctor.objects.get(id=request_data['doctor'])
        appointment.patient = Patient.objects.get(id=request_data['patient'])
        appointment.date = request_data['date']
        appointment.time = request_data['time']
        appointment.status = request_data['status']
        appointment.save()
        return JsonResponse({'message': 'Appointment updated successfully'}, status=200)

    if request.method == 'DELETE':
        request_data = json.loads(request.body.decode('utf-8'))
        appointment = Appointment.objects.filter(id=request_data['id'])
        if not appointment:
            return JsonResponse({ 'message': 'Appointment does not exist'}, status=400)
        appointment.delete()
        return JsonResponse({'message': 'Appointment deleted successfully'}, status=200)

@csrf_exempt
def staff(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        staff = Staff(
            name = request_data['name'],
            role = request_data['role'],
            gender = request_data['gender'],
            phone = request_data['phone'],
            email = request_data['email'],
        )
        staff.save()
        return JsonResponse({'message': 'Staff added successfully'}, status=200)

    if request.method == 'GET':
        staffs = Staff.objects.all()
        response = []
        for staff in staffs:
            response.append({
                'id': staff.id,
                'name': staff.name,
                'role': staff.role,
                'gender':staff.gender,
                'phone': staff.phone,
                'email': staff.email,
            })
        return JsonResponse({'staffs': response}, status=200)

    if request.method == 'PUT':
        request_data = json.loads(request.body.decode('utf-8'))
        staff = Staff.objects.filter(id=request_data['id'])
        if not staff:
            return JsonResponse({ 'message': 'Staff does not exist'}, status=400)
        staff = staff[0]
        staff.name = request_data['name']
        staff.role = request_data['role']
        staff.gender = request_data['gender']
        staff.phone = request_data['phone']
        staff.email = request_data['email']
        staff.save()
        return JsonResponse({'message': 'Staff updated successfully'}, status=200)

    if request.method == 'DELETE':
        request_data = json.loads(request.body.decode('utf-8'))
        staff = Staff.objects.filter(id=request_data['id'])
        if not staff:
            return JsonResponse({ 'message': 'Staff does not exist'}, status=400)
        staff.delete()
        return JsonResponse({'message': 'Staff deleted successfully'}, status=200)


@csrf_exempt
def inventry(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        inventry = Inventry(
            name = request_data['name'],
            type = request_data['type'],
            price = request_data['price'],
            stock = request_data['stock'],
            expiryDate = request_data['expiryDate'],
            manufacturer = request_data['manufacturer'],
        )
        inventry.save()
        return JsonResponse({'message': 'Inventry added successfully'}, status=200)

    if request.method == 'GET':
        inventries = Inventry.objects.all()
        response = []
        for inventry in inventries:
            response.append({
                'id': inventry.id,
                'name': inventry.name,
                'type': inventry.type,
                'price': inventry.price,
                'stock': inventry.stock,
                'expiryDate': inventry.expiryDate,
                'manufacturer': inventry.manufacturer,
            })
        return JsonResponse({'inventries': response}, status=200)

    if request.method == 'PUT':
        request_data = json.loads(request.body.decode('utf-8'))
        inventry = Inventry.objects.filter(id=request_data['id'])
        if not inventry:
            return JsonResponse({ 'message': 'Inventry does not exist'}, status=400)
        inventry = inventry[0]
        inventry.name = request_data['name']
        inventry.type = request_data['type']
        inventry.price = request_data['price']
        inventry.stock = request_data['stock']
        inventry.expiryDate = request_data['expiryDate']
        inventry.manufacturer = request_data['manufacturer']
        inventry.save()
        return JsonResponse({'message': 'Inventry updated successfully'}, status=200)

    if request.method == 'DELETE':
        request_data = json.loads(request.body.decode('utf-8'))
        inventry = Inventry.objects.filter(id=request_data['id'])
        if not inventry:
            return JsonResponse({ 'message': 'Inventry does not exist'}, status=400)
        inventry.delete()
        return JsonResponse({'message': 'Inventry deleted successfully'}, status=200)



@csrf_exempt
def bed(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        bed = Bed(
            roomNumber = request_data['roomNumber'],
            roomType = request_data['roomType'],
            patient = Patient.objects.get(id=request_data['patient']),
            doctor = Doctor.objects.get(id=request_data['doctor']),
            allotmentDate = request_data['allotmentDate'],
            dischargeDate = request_data['dischargeDate'],
        )
        bed.save()
        return JsonResponse({'message': 'Bed added successfully'}, status=200)

    if request.method == 'GET':
        beds = Bed.objects.all()
        response = []
        for bed in beds:
            response.append({
                'id': bed.id,
                'roomNumber': bed.roomNumber,
                'roomType': bed.roomType,
                'patient': {'name':bed.patient.name,'id': bed.patient.id},
                'doctor': {'name':bed.doctor.name, 'id': bed.doctor.id},
                'allotmentDate': bed.allotmentDate,
                'dischargeDate': bed.dischargeDate,
            })
        return JsonResponse({'beds': response}, status=200)

    if request.method == 'PUT':
        request_data = json.loads(request.body.decode('utf-8'))
        bed = Bed.objects.filter(id=request_data['id'])
        if not bed:
            return JsonResponse({ 'message': 'Bed does not exist'}, status=400)
        bed = bed[0]
        bed.roomNumber = request_data['roomNumber']
        bed.roomType = request_data['roomType']
        bed.patient = Patient.objects.get(id=request_data['patient'])
        bed.doctor = Doctor.objects.get(id=request_data['doctor'])
        bed.allotmentDate = request_data['allotmentDate']
        bed.dischargeDate = request_data['dischargeDate']
        bed.save()
        return JsonResponse({'message': 'Bed updated successfully'}, status=200)


    if request.method == 'DELETE':
        request_data = json.loads(request.body.decode('utf-8'))
        bed = Bed.objects.filter(id=request_data['id'])
        if not bed:
            return JsonResponse({ 'message': 'Bed does not exist'}, status=400)
        bed.delete()
        return JsonResponse({'message': 'Bed deleted successfully'}, status=200)


@csrf_exempt
def billing(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        patient = Patient.objects.get(id=request_data['patient'])
        billing = Billing(
            patient = patient,
            doctor = Doctor.objects.get(id=request_data['doctor']),
            department = request_data['department'],
            admissionDate = request_data['admissionDate'],
            dischargeDate = request_data['dischargeDate'],
            costOfTreatment = request_data['costOfTreatment'],
        )
        time = timezone.now()
        generate_bill(billing.patient.name, [billing.admissionDate, billing.dischargeDate], billing.costOfTreatment, patient.name+str(time)+'.pdf')
        billing.bill = patient.name+str(time)+'.pdf'
        billing.save()
        send_mail(
            subject='Billing Details',
            message='Your bill is ready. Please find the attachment'+'  '+ 'http://localhost:8000'+billing.bill.url,
            recipient_list=[patient.email],
            from_email='<from-email>',
        )
        return JsonResponse({'message': 'Billing added successfully'}, status=200)

    if request.method == 'GET':
        billings = Billing.objects.all()
        response = []
        for billing in billings:
            response.append({
                'id': billing.id,
                'patient': {'name':billing.patient.name,'id': billing.patient.id},
                'doctor': {'name':billing.doctor.name, 'id': billing.doctor.id},
                'department': billing.department,
                'admissionDate': billing.admissionDate,
                'dischargeDate': billing.dischargeDate,
                'costOfTreatment': billing.costOfTreatment,
                'bill': billing.bill.url,
            })
        return JsonResponse({'billings': response}, status=200)

    if request.method == 'PUT':
        request_data = json.loads(request.body.decode('utf-8'))
        billing = Billing.objects.filter(id=request_data['id'])
        if not billing:
            return JsonResponse({ 'message': 'Billing does not exist'}, status=400)
        billing = billing[0]
        billing.patient = Patient.objects.get(id=request_data['patient'])
        billing.doctor = Doctor.objects.get(id=request_data['doctor'])
        billing.department = request_data['department']
        billing.admissionDate = request_data['admissionDate']
        billing.dischargeDate = request_data['dischargeDate']
        billing.costOfTreatment = request_data['costOfTreatment']
        billing.save()
        return JsonResponse({'message': 'Billing updated successfully'}, status=200)

    if request.method == 'DELETE':
        request_data = json.loads(request.body.decode('utf-8'))
        billing = Billing.objects.filter(id=request_data['id'])
        if not billing:
            return JsonResponse({ 'message': 'Billing does not exist'}, status=400)
        billing.delete()
        return JsonResponse({'message': 'Billing deleted successfully'}, status=200)

@csrf_exempt
def patient_login(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        if request_data['action']=='sendOtp':

            patient = Patient.objects.filter(email=request_data['email'])
            if not patient:
                return JsonResponse({ 'message': 'Patient does not exist'}, status=400)
            
            send_mail(
                subject='Otp for password reset',
                message='Your otp is 1234',
                recipient_list=[request_data['email']],
                from_email='<from-email>'
            )
            return JsonResponse({'message': 'Password sent to email'}, status=200)
        if request_data['action']=='verifyOtp':
            patient = Patient.objects.filter(email=request_data['email'])
            response={
                'id': patient[0].id,
                'name': patient[0].name,
                'department': patient[0].department,
                'dob': patient[0].dob,
                'gender': patient[0].gender,
                'email': patient[0].email,
                'phone': patient[0].phone,
            }
            return JsonResponse({'patient': response, 'message':'login success'}, status=200)
        

@csrf_exempt
def activity(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()
        appointments = Appointment.objects.all()
    
        billings = Billing.objects.all()
        total = 0
        for billing in billings:
            total += billing.costOfTreatment

        response = {
            'patients': len(patients),
            'doctors': len(doctors),
            'appointments': len(appointments),
            
            'billings': total,
        }
        return JsonResponse({'dashboard': response}, status=200)

@csrf_exempt
def patientCategory(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        neurology = 0
        cardiology = 0
        gastrology = 0
        pulmonology = 0
        emergency = 0
        for patient in patients:
            if patient.department == 'Neurology':
                neurology += 1
            if patient.department == 'Cardiology':
                cardiology += 1
            if patient.department == 'Gastrology':
                gastrology += 1
            if patient.department == 'Pulmonology':
                pulmonology += 1
            if patient.department == 'Emergency':
                emergency += 1
        response = {
            'neurology': neurology,
            'cardiology': cardiology,
            'gastrology': gastrology,
            'pulmonology': pulmonology,
            'emergency': emergency,
        }
        return JsonResponse({'patientCategory': response}, status=200)

def patientRecords(request, id):
    if request.method == 'GET':
        appointments = Appointment.objects.filter(patient=id)
        reports = Report.objects.filter(patient=id)
        bills = Billing.objects.filter(patient=id)
        response={
            'appointments': [],
            'reports': [],
            'bills': []
        }
        for appointment in appointments:
            response['appointments'].append({
                'doctor': appointment.doctor.name,
                'date': appointment.date,
                'time': appointment.time,
                'status': appointment.status
            })
        
        for report in reports:
            response['reports'].append({
                'date': report.date,
                'labTest': report.labTest,
                'report': report.report.url
            })

        for bill in bills:
            response['bills'].append({
                'doctor': bill.doctor.name,
                'department': bill.department,
                'admissionDate': bill.admissionDate,
                'dischargeDate': bill.dischargeDate,
                'costOfTreatment': bill.costOfTreatment,
                'bill': bill.bill.url
            })

        return JsonResponse({'patientDetails': response}, status=200)
