from django.shortcuts import render
import mysql.connector as sql
from django.http import HttpResponse

name =''
sapid=''
roll=''
dept=''
proj=''
group1=''
contact=''
password=''
cpassword=''

# Create your views here.
def signupaction(request):
    global name, sapid, roll, dept, proj, group1, contact, password, cpassword
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="name":
                name=value
            if key == "sapid":
                sapid=value
            if key =="rollno":
                roll=value
            if key =="project":
                proj=value
            if key=="group":
                group1=value
            if key == "contact":
                contact=value
            if key =="password":
                password=value
            if key =="confirmpassword":
                cpassword=value
   
        c = "insert into signup1 values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(name, sapid, roll, dept, proj, group1, contact, password, cpassword)
        cursor.execute(c)
        m.commit()
    return render(request, 'signup_page.html')


def loginaction(request):
    global sapid, password, name,dept, proj
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="name":
                name=value
            if key == "sapid":
                sapid=value
            if key =="password":
                password=value
        c = "select * from Signup1 where sapid='{}' and password='{}'".format(sapid, password)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        print(type(t[0]))
        print(t[0][0])
        print("hello")

        if t ==():
            return render(request, 'error.html')       
        else:
            data={ 
                'title':'Project Mentor Slot Booking',
                'Name': t[0][0],
                'id': sapid,
                'sod': t[0][4],
                'projtil': t[0][3],
                
            }
            print(dict(data))
            return render(request, "Home.html", data)
        
    return render(request, 'Login_page.html')


