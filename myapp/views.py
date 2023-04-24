from django.shortcuts import render
import mysql.connector as sql
from django.http import HttpResponse
from datetime import datetime
from datetime import date
current_date1 = date.today()

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")

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
name1=''
passyear1=''
name1=''
sapid=''
rollno1='' 
dept1='' 
semester1=''
passyear1='' 
ProjectDone1=''
projtitle1=''
contactNo1='' 
password1=''
mentor1=''
email=''
FEmailid1=''

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
                'semester':t[0][5],
                'projtil': t[0][4],
                'tproj':t[0][7],
                'Cproj':"NA",
                'mentor':t[0][9],
                'contno':t[0][8],
                'rollno':t[0][2],
                'pyear':t[0][6],      
            }
            print(dict(data))
            return render(request, "Home.html", data)
        
    return render(request, 'Login_page.html')


def editaction(request):
    global name1, sapid, rollno1, dept1, semester1, passyear1, ProjectDone1, projtitle1, contactNo1, password1, mentor1
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="name1":
                name1=value
            if key =="rollno1":
                rollno1=value
            if key=="dept1":
                dept1=value
            if key =="semester1":
                semester1=value
            if key =="passyear1":
                passyear1=value
            if key =="ProjectDone1":
                ProjectDone1=value                
            if key =="projtitle1":
                projtitle1=value
            if key == "contactNo1":
                contactNo1=value            
            if key == "mentor1":
                mentor1=value
            if key =="password1":
                password1=value

        if name1 !="":
            c = "update signup1 set name='"+name1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if rollno1 !="":
            c = "update signup1 set roll='"+rollno1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if dept1 !="":
            c = "update signup1 set dept='"+dept1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if semester1 !="":
            c = "update signup1 set semester='"+semester1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if passyear1 !="":
            c = "update signup1 set pyear='"+passyear1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if ProjectDone1 !="":
            c = "update signup1 set tproject='"+ProjectDone1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if contactNo1 !="":
            c = "update signup1 set contact='"+contactNo1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if mentor1 !="":
            c = "update signup1 set mentorn='"+mentor1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if password1 !="":
            c = "update signup1 set password='"+password1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()
        if projtitle1 !="":
            c = "update signup1 set proj='"+projtitle1+"' where sapid='"+sapid+"'"
            cursor.execute(c)
            m.commit()

    return render(request, 'editprofile.html')




def senddetails(request):
    global FEmailid, projecttitle, message, member1, member2, member3, member4, member5, Ctime;
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="FEmailid":
                FEmailid=value
            if key == "projecttitle":
                projecttitle=value
            if key =="message":
                message=value
            if key =="member1":
                member1=value
            if key =="member2":
                member2=value
            if key =="member3":
                member3=value
            if key =="member4":
                member4=value
            if key =="member5":
                member5=value
            
        c = "insert into slotbooking values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')".format(FEmailid, projecttitle, message, member1, member2, member3, member4, member5, current_date1, current_time1)
        cursor.execute(c)
        m.commit()
    return render(request, 'sendDetails.html')






def requestaction(request):
    global sapid, password, name,dept, proj
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == "sapid":
                sapid=value
            if key =="password":
                password=value
        c = "select * from Signup1 where sapid='{}' and password='{}'".format(sapid, password)
        cursor.execute(c)
        
        
    return render(request, 'RequestDetailsFac.html')


def slotbookingaction(request):
    global sapid, password, name,dept, proj
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == "sapid":
                sapid=value
            if key =="password":
                password=value
        c = "select * from Signup1 where sapid='{}' and password='{}'".format(sapid, password)
        cursor.execute(c)
        
        
    return render(request, 'FacultySlot.html')


def homeaction(request):
    global sapid, password, name,dept, proj
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == "sapid":
                sapid=value
            if key =="password":
                password=value
        c = "select * from Signup1 where sapid='{}' and password='{}'".format(sapid, password)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        data1={ 
                'title':'Project Mentor Slot Booking',
                'Name': t[0][0],
                'id': sapid,
                'dept': t[0][3],
                'semester':t[0][5],
                'projtil': t[0][4],
                'tproj':t[0][7],
                'Cproj':"NA",
                'mentor':t[0][9],
                'contno':t[0][8],
                'rollno':t[0][2],
                'pyear':t[0][6],      
            }
            
        return render(request, "Home.html", data1)
        
        
    return render(request, 'Home.html')





####################################################################################################################
                             #### Teacher profile works  ####

def loginactionteacher(request):
    global id, password, FEmailid1
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == "id":
                id=value
            if key =="password":
                password=value
        c = "select * from teacher where id='{}' and password='{}'".format(id, password)
        cursor.execute(c)
        t1=tuple(cursor.fetchall())
        FEmailid1=t1[0][3]
        if t1 ==():
            return render(request, 'error.html')       
        else:
            FEmailid1=t1[0][3]
            print(email)
            data1={ 
                'title':'Project Mentor Slot Booking',
                'Name': t1[0][0],
                'id':t1[0][1],
                'dept': t1[0][2],
                'email': t1[0][3],
                'phoneNumber': t1[0][4],
                'office_numer': t1[0][5],
                'total_slot': t1[0][7],
                'fill_slot': t1[0][8],
                
                
            }
            return render(request, "teacherhome.html", data1)
        
    return render(request, 'teacher_login.html')


def teachernewrequests(request):    
    m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
    cursor=m.cursor()
    d=request.POST
    #c = "select * from slotbooking"
    
    c = "select * from slotbooking where FEmailid='{}'".format(FEmailid1)

    cursor.execute(c)
    t=tuple(cursor.fetchall())
    print(t)
    if t ==():
            return render(request, 'error.html')  
    data={
               "data":t
    }
    return render(request, "teacher_newrequest.html", data)

