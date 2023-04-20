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


