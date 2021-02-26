from django.shortcuts import render
from .models import User,Appointment
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
import cv2
def home(request):
    if request.method == 'POST' and 'uid' in request.POST and 'pass' in request.POST:
        u_name = request.POST.get('uid')
        u_pass = request.POST.get('pass')
        try:
            user=User.objects.get(name=u_name)
        except User.DoesNotExist:
            user = None
        if user is not None:
            if u_name == "admin":
                if u_pass == "admin":
                    appointments_obj=Appointment.objects.all()
                    return render(request,'admin.html',{"data":appointments_obj})
            else:
                if u_pass==user.password:
                    # import pdb;pdb.set_trace()
                    return render(request,'appointment.html',{"id":user.id})
                else:
                    messages.info(request, 'Password Does not match.')
        else:
            messages.info(request,'User Does not exist.')

    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def storeuser(request):


    u_name=request.POST.get('uid')
    u_pass=request.POST.get('upassword1')
    u_contact = request.POST.get('ucontact')
    u_email = request.POST.get('uemail')

    user=User(name=u_name,password=u_pass,contact=u_contact,email_id=u_email)
    user.save()
    #import pdb;pdb.set_trace()

    return render(request,'index.html')


def takeappointment(request,id):
    return render(request,'appointment_form.html',{"id":id})

def submitappointment(request,id):
    visit_type = request.POST.get('visit')
    description = request.POST.get('desc')
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    cam = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier('C:/Users/ketul/OneDrive/Desktop/Project_Vedant/demo/haarcascade_frontalface_default.xml')

    count = 0
    while (True):
        ret, img = cam.read()
        faces = face_detector.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces:
            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            count += 1
            user = User.objects.get(id=id)
            cv2.imwrite("C:/Users/ketul/OneDrive/Desktop/Project_Vedant/demo/static/images/" + user.name + ".jpg", img[y1:y2, x1:x2])
            cv2.imshow('image', img)
        k = cv2.waitKey(200) & 0xff
        if k == 27:
            break
        elif count >= 1:
            break
    cam.release()
    cv2.destroyAllWindows()
    user=User.objects.get(id=id)
    #
    appoinments_obj=Appointment(visit_type=visit_type,description=description,date_from=date_from,date_to=date_to,user_id=user)
    appoinments_obj.save()
    messages.info(request, 'Appointment submitted sucessfully.')
    return render(request,'appointment.html',{"id":id})

