from django.shortcuts import render, redirect
import mysql.connector as sql
from django.http import HttpResponse
from datetime import datetime
from datetime import date
import random
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Student, Mentor, Slot, Booking
from .services import SlotBookingService, MentorService, StudentService
from django.contrib.auth import authenticate, login, logout
from .db_utils import DatabaseManager

current_date1 = date.today()
now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")

projectid = random.randint(0,99999999999)

name ='' 
sapid=''
sapid1=''
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
temail=''
totalslot=''
td1=''
tname=''
tid=''
tdept=''
tphoneno=''
officeno=''
totalslot=''
filledslot=''
tpassword='' 
temail=''
filledslot=''

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and isinstance(self.request.user, Student)

class MentorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and isinstance(self.request.user, Mentor)

class StudentDashboardView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    model = Booking
    template_name = 'student/dashboard.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return StudentService.get_student_bookings(self.request.user)

class MentorDashboardView(LoginRequiredMixin, MentorRequiredMixin, ListView):
    model = Booking
    template_name = 'mentor/dashboard.html'
    context_object_name = 'pending_requests'

    def get_queryset(self):
        return MentorService.get_pending_requests(self.request.user)

class CreateSlotView(LoginRequiredMixin, MentorRequiredMixin, CreateView):
    model = Slot
    template_name = 'mentor/create_slot.html'
    fields = ['date', 'start_time', 'end_time']
    success_url = reverse_lazy('mentor_dashboard')

    def form_valid(self, form):
        form.instance.mentor = self.request.user
        return super().form_valid(form)

class BookSlotView(LoginRequiredMixin, StudentRequiredMixin, CreateView):
    model = Booking
    template_name = 'student/book_slot.html'
    fields = ['slot']
    success_url = reverse_lazy('student_dashboard')

    def form_valid(self, form):
        form.instance.student = self.request.user
        booking, message = SlotBookingService.book_slot(
            self.request.user,
            form.cleaned_data['slot']
        )
        if booking:
            messages.success(self.request, message)
            return super().form_valid(form)
        else:
            messages.error(self.request, message)
            return self.form_invalid(form)

class UpdateProjectView(LoginRequiredMixin, StudentRequiredMixin, UpdateView):
    model = Student
    template_name = 'student/update_project.html'
    fields = ['project_title', 'project_description']
    success_url = reverse_lazy('student_dashboard')

    def get_object(self):
        return self.request.user

class AcceptBookingView(LoginRequiredMixin, MentorRequiredMixin, UpdateView):
    model = Booking
    template_name = 'mentor/accept_booking.html'
    fields = []
    success_url = reverse_lazy('mentor_dashboard')

    def form_valid(self, form):
        if self.object.accept():
            messages.success(self.request, "Booking request accepted successfully")
        else:
            messages.error(self.request, "Could not accept the booking request")
        return super().form_valid(form)

class RejectBookingView(LoginRequiredMixin, MentorRequiredMixin, UpdateView):
    model = Booking
    template_name = 'mentor/reject_booking.html'
    fields = []
    success_url = reverse_lazy('mentor_dashboard')

    def form_valid(self, form):
        if self.object.reject():
            messages.success(self.request, "Booking request rejected successfully")
        else:
            messages.error(self.request, "Could not reject the booking request")
        return super().form_valid(form)

# Authentication views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if isinstance(user, Student):
                return redirect('student_dashboard')
            else:
                return redirect('mentor_dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Create your views here.
def signupaction(request):
    if request.method == "POST":
        db = DatabaseManager.get_instance()
        data = request.POST
        
        # Prepare the data
        values = (
            data.get('name', ''),
            data.get('sapid', ''),
            data.get('rollno', ''),
            data.get('dept', ''),
            data.get('project', ''),
            data.get('semester', ''),
            data.get('pyear', ''),
            data.get('tproject', ''),
            data.get('contact', ''),
            data.get('mentorn', ''),
            data.get('password', ''),
            data.get('confirmpassword', '')
        )
        
        # Use parameterized query for security
        query = """
            INSERT INTO signup1 
            (name, sapid, roll, dept, proj, semester, pyear, tproject, contact, mentorn, password, cpassword)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            db.execute_query(query, values)
            messages.success(request, "Registration successful!")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, 'signup_page.html')
            
    return render(request, 'signup_page.html')


def loginaction(request):
    global sapid, password, name,dept, proj, sapid1
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
            sapid1=sapid
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
            cursor.execute(c)
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
    global FEmailid, projecttitle, message, member1, member2, member3, member4, member5, projectid
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
            
        c = "insert into newrequest values('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')".format(projectid,FEmailid, projecttitle, message, member1, member2, member3, member4, member5, current_date1, current_time1)
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
    global sapid, password, name,dept, proj, sapid1
    
    m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
    cursor=m.cursor()
    d=request.POST
    for key,value in d.items():
        if key == "sapid":
            sapid=value
        if key =="password":
            password=value
    c = "select * from Signup1 where sapid='{}'".format(sapid1)
    cursor.execute(c)
    t=tuple(cursor.fetchall())
    data1={ 
            'title':'Project Mentor Slot Booking',
            'Name': t[0][0],
            'id': sapid1,
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


####################################################################################################################
                             #### Teacher profile works  ####

def loginactionteacher(request):
    global id, password, FEmailid1, id1
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
    
    c = "select * from newrequest where FEmailid='{}'".format(FEmailid1)

    cursor.execute(c)
    t=tuple(cursor.fetchall())
    print(t)
    if t ==():
            return render(request, 'error.html')  
    data={
               "data":t
    }
    return render(request, "teacher_newrequest.html", data)



def slotaccepted(request):
    m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
    cursor=m.cursor()
    d=request.POST
    c = "select * from accepted where FEmailid='{}'".format(FEmailid1)
    cursor.execute(c)
    t=tuple(cursor.fetchall())
    print(t)
    if t ==():
            return render(request, 'error.html')
      
    data={
               "data":t
    }
    return render(request, "teacher_slotaccepted.html", data)




def teacherhomeaction(request):
        global id
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        c = "select * from teacher where id='{}'".format(id)
        cursor.execute(c)
        t1=tuple(cursor.fetchall())
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




def teachereditrequest(request):
    global tname, tid, tdept, tphoneno, officeno, totalslot, filledslot, tpassword, temail
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="tname":
                tname=value
            if key =="tid":
                tid=value
            if key=="tdept":
                tdept=value
            if key =="temail":
                temail=value
            if key =="tphoneno":
                tphoneno=value
            if key =="officeno":
                officeno=value                
            if key =="totalslot":
                totalslot=value
            if key == "filledslot":
                filledslot=value            
            if key == "tpassword":
                tpassword=value
            
        if tname !="":
            c = "update teacher set name='"+tname+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
        if tid !="":
            c = "update teacher set id='"+tid+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
        if tdept !="":
            c = "update teacher set department='"+tdept+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
        if temail !="":
            c = "update teacher set email='"+temail+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
        if tphoneno !="":
            c = "update teacher set phoneNumber='"+tphoneno+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
        if officeno !="":
            c = "update teacher set office_number='"+officeno+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
        if totalslot !="":
            c = "update teacher set totalslot='"+totalslot+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
        if filledslot !="":
            c = "update teacher set fillslot='"+filledslot+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
        if tpassword !="":
            c = "update teacher set password='"+tpassword+"' where id='"+id+"'"
            cursor.execute(c)
            m.commit()
       
    return render(request, 'teacher_editprofile.html')



def teacheracceptrequest(request):
    global tname, tdept, tphoneno, officeno, totalslot, filledslot, tpassword, temail, FEmailid1, projecttitle, message, member1, member2, member3, member4, member5, current_date1, current_time1, projectid1
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == "projectid1":
                projectid1=value
        c = "select * from newrequest where projectid='{}'".format(projectid1)
        cursor.execute(c)
        t1=tuple(cursor.fetchall())

        projectid= t1[0][0]
        FEmailid1 = t1[0][1]
        projecttitle = t1[0][2] 
        message = t1[0][3] 
        member1 = t1[0][4] 
        member2 = t1[0][5] 
        member3 = t1[0][6] 
        member4 = t1[0][7] 
        member5 = t1[0][8] 
        current_date1 = t1[0][9] 
        current_time1 = t1[0][10]

        c1 = "insert into accepted values('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')".format(FEmailid1, projectid, projecttitle, message, member1, member2, member3, member4, member5, current_date1, current_time1)
        cursor.execute(c1)
        c3 = "Delete from newrequest where projectid='{}'".format(projectid1)
        cursor.execute(c3)
        m.commit()
      
    return render(request, 'teacherAcceptProject.html')



def teacherrejectrequest(request):
    global tname, tdept, tphoneno, officeno, totalslot, filledslot, tpassword, temail, FEmailid1, projecttitle, message, member1, member2, member3, member4, member5, current_date1, current_time1, projectid1
    if request.method=="POST":
        m = sql.connect(user="root",password="adarshkunal", host="localhost", database="MentorSlotBooking", auth_plugin='mysql_native_password')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == "projectid1":
                projectid1=value
        for key,value in d.items():
            if key == "message":
                message=value
        c = "select * from newrequest where projectid='{}'".format(projectid1)
        cursor.execute(c)
        t1=tuple(cursor.fetchall())

        projectid= t1[0][0]
        FEmailid1 = t1[0][1]
        projecttitle = t1[0][2] 
        member1 = t1[0][4] 
        member2 = t1[0][5] 
        member3 = t1[0][6] 
        member4 = t1[0][7] 
        member5 = t1[0][8] 
        current_date1 = t1[0][9] 
        current_time1 = t1[0][10]

        c2 = "insert into reject values('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')".format(FEmailid1, projectid, projecttitle, message, member1, member2, member3, member4, member5, current_date1, current_time1)
        cursor.execute(c2)
        c3 = "Delete from newrequest where projectid='{}'".format(projectid1)
        cursor.execute(c3)
        m.commit()

      
    return render(request, 'teacherRejectProject.html')



