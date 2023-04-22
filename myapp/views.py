from django.shortcuts import render
import mysql.connector as sql
from django.http import HttpResponse

name =''
sapid=''
roll=''
dept=''
proj=''
semester=''
pyear=''
tproject=''
contact=''
mentorn=''
password=''
cpassword=''

# Create your views here.
def signupaction(request):
    global name, sapid, roll, dept, proj,semester,pyear,tproject,contact,mentorn, password, cpassword
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
            if key=="dept":
                dept=value
            if key =="semester":
                semester=value
            if key =="pyear":
                pyear=value
            if key =="tproject":
                tproject=value                
            if key =="project":
                proj=value
            if key == "contact":
                contact=value            
            if key == "mentorn":
                mentorn=value
            if key =="password":
                password=value
            if key =="confirmpassword":
                cpassword=value
   
        c = "insert into signup1 values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}')".format( name, sapid, roll, dept, proj, semester, pyear, tproject, contact, mentorn, password, cpassword)
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
        if t ==():
            return render(request, 'error.html')       
        else:
            data={ 
                'title':'Project Mentor Slot Booking',
                'Name': t[0][0],
                'id': sapid,
                'dept': t[0][3],
                'projtil': t[0][4],
                
            }
            print(dict(data))
            return render(request, "Home.html", data)
        
    return render(request, 'Login_page.html')


