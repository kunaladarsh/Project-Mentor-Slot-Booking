create database MentorSlotBooking;
use MentorSlotBooking;

create table signup1(name varchar(50), 
sapid varchar(50), 
roll varchar(50),
dept varchar(50),
proj varchar(50), 
semester varchar(50), 
pyear varchar(50),
tproject varchar(50),
contact varchar(50), 
mentorn varchar(50), 
password varchar(50), 
cpassword varchar(50));

select *from Signup1 

create table teacher(name varchar(50), 
id varchar(50), 
department varchar(50),
email varchar(50), 
phoneNumber varchar(50), 
office_number varchar(50),
password varchar(50),
totalslot int(10),
fillslot int(10));

create table slotbooking(FEmailid varchar(50), 
projecttitle varchar(100), 
message varchar(300), 
member1 varchar(50), 
member2 varchar(50), 
member3 varchar(50), 
member4 varchar(50), 
member5 varchar(50), 
current_date1 varchar(50), 
current_time1 varchar(50));

select * from slotbooking
