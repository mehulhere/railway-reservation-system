#conversions
import datetime
import calendar
import random
import inflect
import googlemaps
import difflib
import mysql.connector
from fpdf import FPDF
from datetime import datetime
from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, request, url_for, redirect, session
from flask_executor import Executor
import os
def convertstring(i):
    st = ''
    for item in i:
        st = st + item
    return st

def converttuple(i):
    list = ()
    for item in i:
        list = list + item
    return list

def convertint(i):
    int = 0
    for item in i:
        int = int + item
    return int  

def addcomma(i):
    i="'"+i+"'"
    return i  

#main functions
def time(h1,h2,m1,m2,t):
    mycursor.execute(f'select col from matrix where hour={h1} and minute={m1} and train_no={t}')
    output= mycursor.fetchall()
    n=converttuple(output)
    n=convertint(n)
    mycursor.execute(f'select col from matrix where hour={h2} and minute={m2} and train_no={t}')
    output= mycursor.fetchall()
    s=converttuple(output)
    s=convertint(s)
    hq=[]
    miq=[]
    while n<s:
        mycursor.execute(f'select hour,minute from matrix where col={n} and train_no={t}')
        output= mycursor.fetchall()
        e=converttuple(output)
        h1,m1=e
        mycursor.execute(f'select hour,minute from matrix where col={n+1} and train_no={t}')
        output= mycursor.fetchall()
        f=converttuple(output)
        mi=h=0
        h2,m2=f
        if h1>h2 :
            h=24-h1+h2
        elif h1<=h2:
            h=h2-h1           
        if m1>m2:
            h-=1
            mi=60-m1+m2
        elif m1<m2:
            mi=m2-m1
        n+=1
        hq.append(int(h))
        miq.append(int(mi))
    day = 0
    sum = 0
    for x in hq:
        sum += x
    summ = 0
    for x in miq:
        summ+= x
    if summ>60:
        qa=summ//60
        sum+=qa
        summ=summ-(qa*60)
    if sum>=24:
        we=sum//24
        day=day+we
        sum=sum-(we*24)
    if day==0:
        y=""
    else:
        y=str(day)+" D "
    return(y+str(sum)+" H "+ str(summ)+" M")

def findDay(date):

    d = datetime.strptime(date, '%Y-%m-%d').weekday()
    return (calendar.day_name[d])

def trainname(tn):
    mycursor.execute(f'select train_name from ts where train_no={tn}')
    output= mycursor.fetchall()
    global train_name
    train_name=converttuple(output)
    train_name=convertstring(train_name)
    return(train_name)

def depst(tn,dep_str):
    mycursor.execute(f'select value from matrix where train_no={tn} AND value like {dep_str}')
    output= mycursor.fetchall()
    global departure_station
    departure_station=converttuple(output)
    departure_station=convertstring(departure_station)
    return departure_station

def deptm(tn,dep_str):
    mycursor.execute(f'select hour from matrix where train_no={tn} AND value like {dep_str}')
    h1= mycursor.fetchall()
    h1=converttuple(h1)
    h1=convertint(h1)
    mycursor.execute(f'select minute from matrix where train_no={tn} AND value like {dep_str}')
    m1= mycursor.fetchall()
    m1=converttuple(m1)
    m1=convertint(m1)
    global H1, M1
    H1=str(h1)
    M1=str(m1)
    if len(H1)==1:
        H1=("0"+H1)
    if len(M1)==1:
        M1=("0"+M1)
    return(H1+":"+M1)

def desst(tn,dest_str):
    mycursor.execute(f'select value from matrix where train_no={tn} AND value like {dest_str}')
    output = mycursor.fetchall()
    global destination_station
    destination_station=converttuple(output)
    destination_station=convertstring(destination_station)
    return destination_station

def destm(tn,dest_str):
    mycursor.execute(f'select hour from matrix where train_no={tn} AND value like {dest_str}')
    h2= mycursor.fetchall()
    h2=converttuple(h2)
    h2=convertint(h2)
    mycursor.execute(f'select minute from matrix where train_no={tn} AND value like {dest_str}')
    m2= mycursor.fetchall()
    m2=converttuple(m2)
    m2=convertint(m2)
    global H2, M2
    H2=str(h2)
    M2=str(m2)
    if len(H2)==1:
        H2=("0"+H2)
    if len(M2)==1:
        M2=("0"+M2)
    return(H2+":"+M2)

def distsum(trainno,depst,desst):
    depstt='%'+depst+'%'
    depstt=addcomma(depst)
    mycursor.execute(f'select col from matrix where train_no={trainno} and value like {depstt};')
    output=mycursor.fetchall()
    col=(output[0])
    (j,)=col
    desstt='%'+desst+'%'
    desstt=addcomma(desstt)
    mycursor.execute(f'select col from matrix where train_no={trainno} and value like {desstt};')
    output=mycursor.fetchall()
    col=(output[0])
    (k,)=col
    mycursor.execute(f'select s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15 from ts where train_no={trainno};')
    output=mycursor.fetchall()
    station_list=converttuple(output)
    dist_list=[0.0,]
    for i in range(2,k+1):
        y=float(distance(station_list[i-2],station_list[i-1]))+dist_list[i-2]
        dist_list.append(y)
        global tot_dist
    tot_dist=dist_list[k-1]-dist_list[j-1]

def distance(depst,desst):
    gmaps = googlemaps.Client(key='AIzaSyBThxFy7G1IRYuCeglMolZ_GSSoXus_0Oo')
    my_dist = gmaps.distance_matrix(depst+"Railway Station",desst+"Railway Station")['rows'][0]['elements'][0]['distance']['text']
    my_dist=my_dist.split(" ")
    if float(my_dist[0])>200:
        my_dist[0]=100
    return(my_dist[0])

#maincode

mydb= mysql.connector.connect(host="localhost",user="sqluser",passwd="password",database="rrs")
global Berth,trainnamez,trainno,seat1,seat2,seat3,seat4,seat5,fare,berth1,tot_dist
Berth=["No choice","Lower Berth","Middle Berth","Upper Berth"]
mycursor= mydb.cursor()
s1=s2=s3=s4=s5=s6=s7=s8=s9=s10=s11=s12=s13=s14=s15=''
app = Flask(__name__)
executor = Executor(app)


# @app.route("/train-ticket/")
# def errorgender():
#         return render_template('error.html')

@app.route("/from=to=date=<date>")
def errorinput(date):
        return render_template('error.html')

@app.route("/from=<from1>to=date=<date>")
def errorinputfrom(date,from1):
        return render_template('error.html')

@app.route("/from=to=<to>date=<date>")
def errorinputs(date,to):
        return render_template('error.html')

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/home")

def index2():
    return render_template('index.html')

@app.route("/from=<departure>to=<destination>date=<date>")
def tdr(departure,destination,date):
    global trainname0, trainno0,depst0,deptm0,desst0,destm0,day0,time0,trainname1,trainno1,depst1,deptm1,desst1,destm1,day1,time1,trainname2,trainno2,depst2,deptm2,desst2,destm2,day2,time2,trainname3, trainno3,depst3,deptm3,desst3,destm3,day3,time3,trainname4, trainno4,depst4,deptm4,desst4,destm4,day4,time4,trainname5, trainno5,depst5,deptm5,desst5,destm5,day5,time5,trainname6, trainno6,depst6,deptm6,desst6,destm6,day6,time6,trainname7, trainno7,depst7,deptm7,desst7,destm7,day7,time7,trainname8, trainno8,depst8,deptm8,desst8,destm8,day8,time8,trainname9,trainno9,depst9,deptm9,desst9,destm9,day9,time9
    trainname0=trainno0=depst0=deptm0=desst0=destm0=trainname1=trainno1=depst1=deptm1=desst1=destm1=trainno3=trainname2=trainno2=depst2=deptm2=desst2=destm2=day0=day1=day2=day3=day4=trainname3=depst3=deptm3=desst3=destm3=trainname4=trainno4=depst4=deptm4=desst4=destm4=time3=time1=time2=time0=time4=trainname5=trainno5=depst5=deptm5=desst5=destm5=day5=time5=trainname6=trainno6=depst6=deptm6=desst6=destm6=day6=time6=trainname7=trainno7=depst7=deptm7=desst7=destm7=day7=time7=trainname8=trainno8=depst8=deptm8=desst8=destm8=day8=time8=trainname9=trainno9=depst9=deptm9=desst9=destm9=day9=time9='g'
    mycursor.execute(f'select distinct value from matrix')
    output=mycursor.fetchall()
    train_names=converttuple(output)
    departure=(departure).upper()
    destination=(destination).upper()
    y=difflib.get_close_matches(departure,train_names)
    z=difflib.get_close_matches(destination,train_names)
    if len(y)==0:
        return render_template('error.html')
    if len(z)==0:
        return render_template('error.html')
    departure=convertstring(y[0])
    destination=convertstring(z[0])
    dep_str=("'%"+ departure + "%'")
    dest_str=("'%"+ destination + "%'")
    day1=str(findDay(date))
    day=day1[:2]
    day=("'%"+day+"%'")
    mycursor.execute(f'select train_no from ts where (s1 like {dep_str} or s2 like {dep_str} or s3 like {dep_str} or s4 like {dep_str} or s5 like {dep_str} or s6 like {dep_str} or s7 like {dep_str} or s8 like {dep_str} or s9 like {dep_str} or s10 like {dep_str} or s11 like {dep_str} or s12 like {dep_str} or s13 like {dep_str} or s14 like {dep_str} or s15 like {dep_str}) AND (s1 like {dest_str} or s2 like {dest_str} or s3 like {dest_str} or s4 like {dest_str} or s5 like {dest_str} or s6 like {dest_str} or s7 like {dest_str} or s8 like {dest_str} or s9 like {dest_str} or s10 like {dest_str} or s11 like {dest_str} or s12 like {dest_str} or s13 like {dest_str} or s14 like {dest_str} or s15 like {dest_str}) AND (DAYS like {day} or DAYS="DAILY")')
    output= mycursor.fetchall()
    train_nos=converttuple(output)
    train_nos=list(train_nos)
    x=0
    for tn in train_nos:
        mycursor.execute(f'select col from matrix where train_no={tn} and (value like {dep_str})')
        output = mycursor.fetchall()
        departure_col=(output[0])
        mycursor.execute(f'select col from matrix where train_no={tn} and (value like {dest_str})')
        output= mycursor.fetchall()
        destination_col=(output[0])
        if destination_col==departure_col:
            return render_template('error.html')
        elif departure_col < destination_col:
            tn=(str(tn))
            if len(tn)==4:
                tn=("0"+ str(tn))
            mycursor.execute(f'select DAYS from ts where train_no={tn}')
            output=mycursor.fetchall()
            day=converttuple(output)
            day=convertstring(day)
            s="trainno"
            t=(str(s)+str(x))
            globals()[t]=tn
            s="trainname"
            t=(str(s)+str(x))
            globals()[t]=trainname(tn)
            s="depst"
            t=(str(s)+str(x))
            globals()[t]=depst(tn,dep_str)
            s="deptm"
            t=(str(s)+str(x))
            globals()[t]=deptm(tn,dep_str)
            s="desst"
            t=(str(s)+str(x))
            globals()[t]=desst(tn,dest_str)
            s="destm"
            t=(str(s)+str(x))
            globals()[t]=destm(tn,dest_str)
            s="day"
            t=(str(s)+str(x))
            if day=="DAILY":
                day="Su Mo Tu We Th Fr Sa"
            globals()[t]=day
            mycursor.execute(f'select hour from matrix where train_no={tn} AND value like {dep_str}')
            h1= mycursor.fetchall()
            h1=(h1[0])
            h1=convertint(h1)
            mycursor.execute(f'select minute from matrix where train_no={tn} AND value like {dep_str}')
            m1 = mycursor.fetchall()
            m1=(m1[0])
            m1=convertint(m1)
            global H1, M1
            H1=str(h1)
            M1=str(m1)
            if len(H1)==1:
                H1=("0"+H1)
            if len(M1)==1:
                M1=("0"+M1)
            mycursor.execute(f'select col from matrix where train_no={int(tn)}')
            output = mycursor.fetchall()
            output=converttuple(output)
            g=len(output)
            mycursor.execute(f'select hour from matrix where train_no={int(tn)} AND value like {dest_str}')
            h2 = mycursor.fetchall()
            h2=(h2[0])
            h2=convertint(h2)
            mycursor.execute(f'select minute from matrix where train_no={int(tn)} AND value like {dest_str}')
            m2 = mycursor.fetchall()
            m2=(m2[0])
            m2=convertint(m2)
            global H2, M2
            H2=str(h2)
            M2=str(m2)
            if len(H2)==1:
                H2=("0"+H2)
            if len(M2)==1:
                M2=("0"+M2)
            s="time"
            t=(str(s)+str(x))
            globals()[t]=time(H1,H2,M1,M2,int(tn))  
            x+=1
    return render_template('trainsearch.html', **globals() ,space=" ",date=date,k=x)

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/listtrains")
def listtrain():
    global tn
    mycursor.execute(f'select train_no from ts')
    output = mycursor.fetchall()
    train_list=converttuple(output)
    for tn in train_list:
        global x
        x = train_list.index(int(tn))
        s="trainno"
        t=(str(s)+str(x))
        globals()[t]=tn
        mycursor.execute(f'select train_name from ts where train_no={int(tn)}')
        output = mycursor.fetchall()
        output=converttuple(output)
        s="trainname"
        t=(str(s)+str(x))
        globals()[t]=convertstring(output)
        mycursor.execute(f'select days from ts where train_no={int(tn)}')
        output = mycursor.fetchall()
        output=converttuple(output)
        s="day"
        t=(str(s)+str(x))
        globals()[t]=convertstring(output)
        mycursor.execute(f'select hour from matrix where train_no={tn} AND col=1')
        h1= mycursor.fetchall()
        h1=converttuple(h1)
        h1=convertint(h1)
        mycursor.execute(f'select minute from matrix where train_no={tn} AND col=1')
        m1 = mycursor.fetchall()
        m1=converttuple(m1)
        m1=convertint(m1)
        global H1, M1
        H1=str(h1)
        M1=str(m1)
        if len(H1)==1:
            H1=("0"+H1)
        if len(M1)==1:
            M1=("0"+M1)
        mycursor.execute(f'select col from matrix where train_no={int(tn)}')
        output = mycursor.fetchall()
        output=converttuple(output)
        g=len(output)
        mycursor.execute(f'select hour from matrix where train_no={int(tn)} AND col={g}')
        h2 = mycursor.fetchall()
        h2=converttuple(h2)
        h2=convertint(h2)
        mycursor.execute(f'select minute from matrix where train_no={int(tn)} AND col={g}')
        m2 = mycursor.fetchall()
        m2=converttuple(m2)
        m2=convertint(m2)
        global H2, M2
        H2=str(h2)
        M2=str(m2)
        if len(H2)==1:
            H2=("0"+H2)
        if len(M2)==1:
            M2=("0"+M2)
        s="time"
        t=(str(s)+str(x))
        globals()[t]=time(H1,H2,M1,M2,int(tn))
    return render_template('listtrains.html', **globals())
@app.route("/inserttrain")

def inserttrain():
    return render_template('inserttrain.html')

@app.route("/inserttrain/trainno=<Trainno>trainame=<Trainamez>s1=<S1>s2=<S2>s3=<S3>s4=<S4>s5=<S5>s6=<S6>s7=<S7>s8=<S8>s9=<S9>s10=<S10>s11=<S11>s12=<S12>s13=<S13>s14=<S14>s15=<S15>t1=<t1>t2=<t2>t3=<t3>t4=<t4>t5=<t5>t6=<t6>t7=<t7>t8=<t8>t9=<t9>t10=<t10>t11=<t11>t12=<t12>t13=<t13>t14=<t14>t15=<t15>days=<DAY>")
def inserttrainextension(Trainamez,Trainno,S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,DAY):
    global Trainnamez
    Trainnamez=Trainamez.lstrip()
    trainno=int(Trainno)
    train_name=addcomma(Trainamez).upper()
    S1=addcomma(S1.lstrip()).upper()
    S2=addcomma(S2.lstrip()).upper()
    S3=addcomma(S3.lstrip()).upper()
    S4=addcomma(S4.lstrip()).upper()
    S5=addcomma(S5.lstrip()).upper()
    S6=addcomma(S6.lstrip()).upper()
    S7=addcomma(S7.lstrip()).upper()
    S8=addcomma(S8.lstrip()).upper()
    S9=addcomma(S9.lstrip()).upper()
    S10=addcomma(S10.lstrip()).upper()
    S11=addcomma(S11.lstrip()).upper()
    S12=addcomma(S12.lstrip()).upper()
    S13=addcomma(S13.lstrip()).upper()
    S14=addcomma(S14.lstrip()).upper()
    S15=addcomma(S15.lstrip()).upper()
    day=addcomma(DAY.lstrip()).capitalize()
    mycursor.execute(f'insert into ts values({trainno},{train_name},{S1},{S2},{S3},{S4},{S5},{S6},{S7},{S8},{S9},{S10},{S11},{S12},{S13},{S14},{S15},{day});')
    t=[t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15]
    for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
        l=[]
        for ch in t[i-1]:
            if ch != ":":
                l.append(ch)
        if len(l)==3:
            l.insert(0,"0")
        elif len(l)==4:
            pass
        elif len(l)==5:
            l.pop(0)
        else:
            break
        hour=l[0]+l[1]
        minute=l[2]+l[3]
        mycursor.execute(f'select s{i} from ts where train_no={trainno}')
        output = mycursor.fetchone()
        station = convertstring(output)
        station= addcomma(station)
        pk=(str(trainno)+str(i))
        pk=addcomma(pk)
        mycursor.execute(f'insert into matrix values({pk},{trainno}, {i}, {station},{hour},{minute});')
    mydb.commit()
    return render_template('insertedtrain.html', Trainnamez=Trainnamez)
    
@app.route("/insertedtrain")
def inserttedrain():
    return render_template('insertedtrain.html',Trainnamez=Trainnamez)

@app.route("/inserttrain/trainno=<trainno>")
def insertrtaincheck(trainno):
    mycursor.execute(f'select train_name from ts where train_no={trainno}')
    output = mycursor.fetchone()
    if output==None:
        k=" has NOT been Added"
    else:
        k="is already Added"
    return render_template('inserttraincheck.html',trainno=trainno, k=k)

@app.route("/undefinedtrainname=<trainnamez>trainno=<trainno>deptm=<deptm>destm=<destm>depst=<depst>desst=<desst>")
def trainroute(trainnamez,trainno,deptm,destm,depst,desst):
    global s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15
    s1=s2=s3=s4=s5=s6=s7=s8=s9=s10=s11=s12=s13=s14=s15=k1=k2=k3=k4=k5=k6=k7=k8=k9=k10=k11=k12=k13=k14=k15='l'
    depst='%'+depst+'%'
    depst=addcomma(depst)
    desst='%'+desst+'%'
    desst=addcomma(desst)
    mycursor.execute(f'select col from matrix where train_no={trainno} and value like {depst};')
    output=mycursor.fetchall()
    col=(output[0])
    s="k"
    (i,)=col
    t=(str(s)+str(i))
    globals()[t]=1
    mycursor.execute(f'select col from matrix where train_no={trainno} and value like {desst};')
    output=mycursor.fetchall()
    col=(output[0])
    (i,)=col
    t=(str(s)+str(i))
    globals()[t]=1
    mycursor.execute(f'select s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15 from ts where train_no={trainno};')
    output=mycursor.fetchall()
    station_list=converttuple(output)
    l=(sum(1 for x in station_list if x != '' and x!=' ' and x!='  '))
    for i in range(1,l+1):
        s="s"
        t=(str(s)+str(i))
        globals()[t]=station_list[i-1]
    dist_list=[0.0,]
    for i in range(2,l+1):
        s="d"
        t=(str(s)+str(i))
        globals()[t]=round(float(distance(station_list[i-2],station_list[i-1]))+dist_list[i-2],1)
        dist_list.append(globals()[t])
    for i in range(1,l+1):
        n=station_list[i-1]
        n=addcomma(n)
        s="t"
        t=(str(s)+str(i))
        mycursor.execute(f'select hour,minute from matrix where train_no={trainno} and value={n};')
        output=mycursor.fetchall()
        time_list=converttuple(output)
        H1=str(time_list[0])
        M1=str(time_list[1])
        if len(H1)==1:
            H1=("0"+H1)
        if len(M1)==1:
            M1=("0"+M1)
        globals()[t]=str(H1)+':'+str(M1)
    return render_template('viewroute.html',**globals(),trainnamez=trainnamez,trainno=trainno,space=" ",dist_list=dist_list)

@app.route("/undefinedtrainname=<trainnamez>trainno=<trainno>deptm=<deptm>destm=<destm>depst=<depst>desst=<desst>time=<time>day=<day>date=<date>",methods=["POST", "GET"])
def booktrain(trainnamez,trainno,deptm,destm,depst,desst,time,day,date):
    executor.submit(distsum(trainno,depst,desst))
    return render_template('booktrain.html', space=" ",trainnamez=trainnamez,trainno=trainno,deptm=deptm,destm=destm,depst=depst,desst=desst,time=time,day=day,date=date)
    
@app.route("/train-ticket")
def ticketsuccess():
    trainnamez = request.args.get('trainname')
    trainno = request.args.get('trainno')
    fname = request.args.get('fullname')
    age = request.args.get('age')
    gender = request.args.get('gender')
    berth1 = request.args.get('berth')
    depst = request.args.get('depst')
    desst = request.args.get('desst')
    time = request.args.get('time')
    deptm = request.args.get('deptm')
    destm = request.args.get('destm')
    class1 = request.args.get('class')  
    date = request.args.get('date')
    mno = request.args.get('mno')
    add = request.args.get('add')
    name2 = request.args.get('name2')
    age2 = request.args.get('age2')
    gender2 = request.args.get('gender2')
    berth2 = request.args.get('berth2')
    name3 = request.args.get('name3')
    age3 = request.args.get('age3')
    gender3 = request.args.get('gender3')
    berth3 = request.args.get('berth3')
    name4 = request.args.get('name4')
    age4 = request.args.get('age4')
    gender4 = request.args.get('gender4')
    berth4 = request.args.get('berth4')
    name5 = request.args.get('name5')
    age5 = request.args.get('age5')
    gender5 = request.args.get('gender5')
    berth5 = request.args.get('berth5')
    for i in range (2,6): 
        s="name"
        t=(str(s)+str(i))
        if locals()[t]=="0":
            passenger=i-1
            break
    else:
        passenger=5
    seat1=random.randint(1,100)
    s="seat"
    for i in range(1,6):
        t=(str(s)+str(i))
        globals()[t]=''
        if int(passenger)>=i:
            t=(str(s)+str(i))
            globals()[t]=str(seat1+(i-1))
    qouta="GN"
    berth_list=("LB","MB","UB")
    if berth1=="0":
        berth1=berth_list[random.randint(0,2)]
    if berth2=="0":
        berth2=berth_list[random.randint(0,2)]
    if berth3=="0":
        berth3=berth_list[random.randint(0,2)]
    if berth4=="0":
        berth4=berth_list[random.randint(0,2)]
    if berth5=="0":
        berth5=berth_list[random.randint(0,2)]
    tid=int(str(10000)+str(random.randint(1111111111,9999999999)))
    nameno=trainno+"/"+trainnamez
    dttm=date+", "+str(deptm)
    time1=time.split(" ")
    # if int(time1[2])>23:
    #     date=date.split("-")
    #     date[2]=str(int(date[2])+1)
    #     date="-".join(date)
    dstm=date+', '+str(destm)
    coach_list=['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10','S11','S12']
    coach=coach_list[random.randint(1,11)]
    if class1=="2S":
        y=30+tot_dist*0.4
    elif class1=="CC":
        y=60+tot_dist*1
    elif class1=="SL":
        y=120+tot_dist*0.478
    elif class1=="3AC":
        y=150+tot_dist*1.2
    elif class1=="2AC":
        y=250+tot_dist*2
    y=round(y)
    y=str(y)+"."+str(random.randint(11,99))
    fare=float(y)
    fare=fare*int(passenger)
    fare=round(fare,2)
    pnr=random.randint(1111111111,9999999999)
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    fare1=17.71
    fare2=2.94
    faret=fare+fare1+fare2
    faret=round(faret,2)
    n2w = inflect.engine()
    pdf = FPDF()
    global run
    run=0
    def np(i):
            if i>270:
                    newpage()
                    global run
                    i=i-265
                    return i
            else:
                    return i
    def newpage():
            global run
            while run==0:
                    run+=1
                    pdf.add_page()
                    pdf.rect( x=3,y=3,w=204, h=291, style = '')
            else:
                    pass
    pdf.add_page()
    pdf.rect( x=3,y=3,w=204, h=291, style = '')
    current_directory = os.getcwd()
    print(current_directory)
    pdf.image(name=current_directory + '\\IRCTC-Logo-PNG-Color.png', x=192, y=4, w=12, h=15)
    pdf.image(name=current_directory + '\\Railway.jpeg', x=6, y=5, w=11, h=11)
    pdf.image(name=current_directory + '\\qr.png', x=183, y=30, w=20, h=20)
    pdf.set_font('Arial', '', 11)
    pdf.set_font('', 'UB')
    pdf.set_left_margin(80)
    pdf.write(4, 'IRCTCs e-Ticketing Service')
    pdf.set_xy(65,14)
    pdf.write(13, 'Electronic Reservation Slip(Personal User)')
    pdf.set_font("Arial", size = 6.5)
    pdf.set_text_color(0, 0, 0)    
    pdf.text(1, 30, txt = "          1. This Ticket will be valid with an ID proof in original. Please carry original Identity Proof. If found traveling without original ID proof Passenger will be treated as without ")
    pdf.text(1, 33, txt = "              ticket and charged as per extent Railway Rules.")
    pdf.text(1, 38, txt = '          2. Valid IDs to be presented during train journey by one of the passenger booked on an e-ticket - Voter Identity Card / Passport / PAN Card / Driving License / Photo ID')
    pdf.text(1, 41, txt = '              card issued by Central/State Govt/ Public Sector Undertakings of State / Central Government District Administrations, Municipal bodies and Panchayat Administrations')
    pdf.text(1, 44, txt = '              which are having serial number / Student Identity Card with photograph issued by recognized School or College for their students / Nationalized Bank Passbook with ')
    pdf.text(1, 47, txt = '              photograph/Credit Cards issued by Banks with laminated photograph/Unique Identification Card "Aadhaar". ')
    pdf.text(1, 52, txt = '          3. Service Accounting Code (SAC) 996411: Local land transport services of passengers by railways for distance upto 150 KMs Service Accounting Code (SAC) 996416:')
    pdf.text(1, 55, txt = '              Sightseeing transportation services by railways for Tourist Ticket Service Accounting Code (SAC) 996421: Long distance transport services of passengers through rail')
    pdf.text(1, 58, txt = '              network by Railways for distance beyond 150 KMS ')
    pdf.text(1, 63, txt = '          4. In case the ticket has been booked in advance before implementation of GST and the same is cancelled after implementation of GST, Refund amount due as per refund')
    pdf.text(1, 66, txt = '              shall be refunded to passenger. However total amount of service change charged at the time of booking shall not be refunded to passenger in cash/ shall not be')
    pdf.text(1, 69, txt = '              transferred in the account in which transaction took place in case of e-Tickets etc. ')
    pdf.text(1, 74, txt = '          5. Refund of service tax shall be made only after Ministry of Railways gets refund from the department. The cancelled ticket shall be treated be as credit note')
    pdf.text(1, 77, txt = '              for getting refund of service tax amount.')
    pdf.text(1, 82, txt = '          6. General rules/ Information for e-ticket passenger have to be studied by the customer for cancellation & refund.',
            )   
    pdf.set_xy(6,85)
    pdf.set_font('', 'B',7)
    pdf.cell(66,4, txt = 'PNR NO: %d' %pnr,border=1,align='L')
    pdf.set_font('', '',7)
    pdf.cell(66,4, txt = 'Train No. & Name: %s'%nameno,border=1)
    pdf.cell(66,4, txt = 'Qouta: %s'%qouta,border=1)
    pdf.set_xy(6,89)
    pdf.set_font('', 'B',7)
    pdf.cell(66,4, txt = 'Transaction ID: %d'%tid,border=1,align='L')
    pdf.set_font('', '',7)
    pdf.cell(66,4, txt = 'Date & Time of Booking: %s'%dt_string,border=1)
    pdf.cell(66,4, txt = 'Class: %s'%class1,border=1)
    pdf.set_xy(6,93)
    pdf.cell(66,4, txt = 'From: %s'%depst,border=1,align='L')
    pdf.cell(66,4, txt = 'Date of Journey: %s'%date,border=1)
    pdf.cell(66,4, txt = 'To: %s'%desst,border=1)
    pdf.set_xy(6,97)
    pdf.cell(66,4, txt = 'Boarding: %s'%depst,border=1,align='L')
    pdf.cell(66,4, txt = 'Date of Boarding: %s'%date,border=1)
    pdf.cell(66,4, txt = 'Scheduled Departure: %s'%dttm,border=1)
    pdf.set_xy(6,101)
    pdf.cell(66,4, txt = 'Resv. Up to : %s'%desst,border=1,align='L')
    pdf.cell(66,4, txt = 'Scheduled Arrival: %s'%dstm,border=1)
    pdf.cell(66,4, txt = '%s Adult 0 Child '%passenger,border=1)
    pdf.set_xy(6,105)
    pdf.cell(66,4, txt = 'Passenger Mobile No: %d'%int(mno),border=1,align='L')
    pdf.cell(66,4, txt = 'Note:- N/A',border=1)
    pdf.cell(66,4, txt = 'Distance: %s km(s) '%round(tot_dist,1),border=1)
    pdf.set_xy(6,109)
    pdf.set_font('', 'B',7)
    pdf.cell(66,4, txt = 'Passenger Address: ',border=1,align='L')
    pdf.set_font('', '',7)
    add=add.replace("%","/")
    pdf.cell(132,4, txt = '%s'%add,border=1)
    pdf.set_xy(6,113)
    pdf.cell(198,4, txt = ' ',border=1,align='L')
    pdf.set_xy(6,118)
    pdf.set_font('', 'B',9)
    pdf.cell(66,5, txt = 'FARE DETAILS: ',border=0,)
    pdf.set_font('', 'B',8)
    pdf.set_xy(6,124)
    pdf.cell(83,5, txt = 'Ticket Fare: ',border=1,align='L')
    pdf.cell(17,5, txt = '%s'%fare,border=1)
    
    r1=[(n2w.number_to_words(fare)),(n2w.number_to_words(fare1)),(n2w.number_to_words(fare2)),(n2w.number_to_words(faret))]
    l=0
    k=""
    for i in r1:
        b=[]
        for el in i.split(" "):
            el=el.capitalize()
            if el=="And":
                el=""
            if el=="Point":
                el="And"
                k="Paise"
            b.append(el)
        b.append(k)
        i=" ".join(b)
        i=i.replace("  "," ")
        r1[l]=i
        l+=1   
    pdf.cell(98,5, txt = 'Rupees %s Only'%r1[0],border=1)
    pdf.set_xy(6,129)
    pdf.cell(83,5, txt = 'IRCTC Service Charge (Incl. of Service Tax) #',border=1,align='L')
    pdf.cell(17,5, txt = '%s'%fare1,border=1)
    pdf.cell(98,5, txt = 'Rupees %s Only'%r1[1],border=1)
    pdf.set_xy(6,134)
    pdf.cell(83,5, txt = 'Travel Insurance Premium (Incl. of Service Tax)',border=1,align='L')
    pdf.cell(17,5, txt = '%s'%fare2,border=1)
    pdf.cell(98,5, txt = 'Rupees %s Only'%r1[2],border=1)
    pdf.set_xy(6,139)
    pdf.cell(83,5, txt = 'Total Fare (All inclusive)',border=1,align='L')
    pdf.cell(17,5, txt = '%s'%faret,border=1)
    pdf.cell(98,5, txt = 'Rupees %s Only'%r1[3],border=1)
    pdf.set_xy(5,150)
    pdf.set_font('', '',7)
    pdf.cell(66,5, txt = '# Service Charges per e-ticket irrespective of number of passengers on the ticket.',border=0,)
    pdf.set_xy(6,161)
    pdf.set_font('', 'B',9)
    pdf.cell(66,5, txt = 'PASSENGER DETAILS:',border=0,)
    pdf.set_xy(6,167)
    pdf.set_font('', 'B',7)
    pdf.cell(15,5, txt = 'SNo.',border=1,align='C')
    pdf.cell(60,5, txt = 'Name',border=1,align='C')
    pdf.cell(16,5, txt = 'Age',border=1,align='C')
    pdf.cell(18,5, txt = 'Sex',border=1,align='C')
    pdf.cell(45,5, txt = 'Booking Status',border=1,align='C')
    pdf.cell(45,5, txt = 'Current Status',border=1,align='C')
    pdf.set_font('', '',7)
    pdf.set_xy(6,172)
    pdf.cell(15,5, txt = '1',border=1,align='C')
    pdf.cell(60,5, txt = '%s'%fname,border=1,align='C')
    pdf.cell(16,5, txt = '%s'%age,border=1,align='C')
    pdf.cell(18,5, txt = '%s'%gender,border=1,align='C')
    pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat1 ,berth1),border=1,align='C')
    pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach, seat1,berth1),border=1,align='C')
    x=int(passenger)
    y=5
    if x>1:
            pdf.set_xy(6,177)
            pdf.cell(15,5, txt = '2',border=1,align='C')
            pdf.cell(60,5, txt = '%s'%name2,border=1,align='C')
            pdf.cell(16,5, txt = '%s'%age2,border=1,align='C')
            pdf.cell(18,5, txt = '%s'%gender2,border=1,align='C')
            pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat2 ,berth2),border=1,align='C')
            pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat2 ,berth2),border=1,align='C')
    if x>2:
            pdf.set_xy(6,182)
            pdf.cell(15,5, txt = '3',border=1,align='C')
            pdf.cell(60,5, txt = '%s'%name3,border=1,align='C')
            pdf.cell(16,5, txt = '%s'%age3,border=1,align='C')
            pdf.cell(18,5, txt = '%s'%gender3,border=1,align='C')
            pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat3 ,berth3),border=1,align='C')
            pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat3 ,berth3),border=1,align='C')
    if x>3:
            pdf.set_xy(6,187)
            pdf.cell(15,5, txt = '4',border=1,align='C')
            pdf.cell(60,5, txt = '%s'%name4,border=1,align='C')
            pdf.cell(16,5, txt = '%s'%age4,border=1,align='C')
            pdf.cell(18,5, txt = '%s'%gender4,border=1,align='C')
            pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat4 ,berth4),border=1,align='C')
            pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat4 ,berth4),border=1,align='C')
    if x>4:
            pdf.set_xy(6,192)
            pdf.cell(15,5, txt = '5',border=1,align='C')
            pdf.cell(60,5, txt = '%s'%name5,border=1,align='C')
            pdf.cell(16,5, txt = '%s'%age5,border=1,align='C')
            pdf.cell(18,5, txt = '%s'%gender5,border=1,align='C')
            pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat5 ,berth5),border=1,align='C')
            pdf.cell(45,5, txt = 'CNF/%s/%s/%s'%(coach ,seat5 ,berth5),border=1,align='C')
    pdf.set_xy(5,173+(x*y))
    pdf.set_font('', 'BU',7)
    pdf.cell(0,5, txt = 'This ticket is booked on a personal user ID and cannot be sold by an agent. If bought from an agent by any individual, it is at his/her own risk.',border=0,align='L')
    pdf.set_xy(5,180+(x*y))
    pdf.set_font('', 'B',8)
    pdf.cell(0,5, txt = 'Ticket Printing TIme:')
    pdf.set_font('', '',8)
    dt_string=str(dt_string)
    pdf.set_xy(34,180+(x*y))
    pdf.cell(0,5, txt = '%s'%dt_string)
    pdf.set_text_color(228, 43, 0)
    pdf.set_font('', '',9)
    pdf.set_xy(5,188+(x*y))
    pdf.cell(0,5, txt = 'IR recovers only 57% of cost of travel on an average')
    pdf.set_xy(5,196+(x*y))
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('', 'B',9)
    pdf.cell(0,5,txt='IMPORTANT:')
    pdf.set_xy(5,204+(x*y))
    pdf.set_font('', '',6.5)
    pdf.cell(0,4, txt = "1. For details, rules and terms & conditions of E-Ticketing services, please visit www.irctc.co.in")
    pdf.set_xy(5,208+(x*y))
    pdf.cell(0,4, txt = "2. 'New Time Table will be effective from 1-Oct-2017. Departure time and Arrival Time printed on this ERS/VRM is liable to change. Please check correct departure, arrival from Railway Station")
    pdf.set_xy(5,211+(x*y))
    pdf.cell(0,4, txt = "Enquiry Dial 139 or SMS RAIL to 139.")
    pdf.set_xy(5,215+(x*y))
    pdf.cell(0,4, txt = "3. There are amendments in certain provision of Refund Rules. Refer Amended Refund Rules w.e.f 12-Nov-2015.(details available on www.irctc.co.in under heading Refund Rule--> Cancellation ")
    pdf.set_xy(5,218+(x*y))
    pdf.cell(0,4, txt = "of Ticket and Refund Rules 2015.) ")
    pdf.set_xy(5,222+(x*y))
    pdf.cell(0,4, txt = "4. The accommodation booked is not transferable and is valid only if the ORIGINAL ID card prescribed is presented during the journey. The ERS/VRM/MRM along with valid id card') of any one")
    pdf.set_xy(5,225+(x*y))
    pdf.cell(0,4, txt = "the passenger booked on e-ticket proof in original would be verified by TTE with the name and PNR on the chart. If the Passenger fail to produced/display ERS/VRM due to any eventuality(loss,")
    pdf.set_xy(5,228+(x*y))
    pdf.cell(0,4, txt = "damaged mobile/laptop etc.) but has the prescribed original proof of identity, a penalty of Rs.50/- per ticket as applicable to such cases will be levied. The ticket checking staff on board/off board")
    pdf.set_xy(5,231+(x*y))
    pdf.cell(0,4, txt = "will give excess fare ticket for the same. ")
    pdf.set_xy(5,np(235+(x*y)))
    pdf.cell(0,4, txt = "5. E-ticket cancellations are permitted through www.irctc.co.in by the user. ")
    pdf.set_xy(5,np(239+(x*y)))
    pdf.cell(0,4, txt = "6. PNRs having fully waitlisted status will be dropped and the names of the passengers will not appear on the chart. They are not allowed to board the train. However the namesof PARTIALLY ")
    pdf.set_xy(5,np(242+(x*y)))
    pdf.cell(0,4, txt = "waitlisted/confirmed and RAC will appear in the chart.")
    pdf.set_xy(5,np(246+(x*y)))
    pdf.cell(0,4, txt = "7. Obtain certificate from the TTE/Conductor in case of (a) PARTIALLY waitlisted e-ticket when LESS NO. OF PASSENGERS travel. (b)A.C.FAILURE, (C)TRAVEL IN LOWER CLASS. This")
    pdf.set_xy(5,np(249+(x*y)))
    pdf.cell(0,4, txt = "original certificate must be sent to GGM (IT), IRCTC, Internet Ticketing Centre, IRCA Building, State Entry Road, New Delhi-110055 after filing TDR online within prescribed time for claiming refund")
    pdf.set_xy(5,np(253+(x*y)))
    pdf.cell(0,4, txt = "8. In case of Partial confirmed/RAC/Wait listed ticket, TDR should be filed online within prescribed time in case NO PASSENGER is travelling for processing of refund as per Railway refund rules")
    pdf.set_xy(5,np(257+(x*y)))
    pdf.cell(0,4, txt = "9. While TDR refund requests are filed & registered on IRCTC website www.irctc.co.in, they are processed by Zonal Railways as per Railway Refund Rules (detail available on www.irctc.co.in under") 
    pdf.set_xy(5,np(260+(x*y)))
    pdf.cell(0,4, txt = "heading General Information.")
    pdf.set_xy(5,np(264+(x*y)))
    pdf.cell(0,4, txt = "10. In premium special train cancellation is not allowed.") 
    pdf.set_xy(5,np(268+(x*y)))
    pdf.cell(0,4, txt = "11. No refund shall be granted on the confirmed ticket after four hours before the scheduled departure of the train.")
    pdf.set_xy(5,np(272+(x*y)))
    pdf.add_page
    pdf.cell(0,4, txt = "12. No refund shall be granted on the RAC or Waitlisted ticket after thirty minutes before the scheduled departure of the train.")
    pdf.set_xy(5,np(276+(x*y)))
    pdf.cell(0,4, txt = "13. In case, on a party e-ticket or a family e-ticket issued for travel of more than one passenger, some passengers have confirmed reservation and others are on RAC or waiting list, full refund")
    pdf.set_xy(5,np(279+(x*y)))
    pdf.cell(0,4, txt = "of fare , less clerkage, shall be admissible for confirmed passengers also subject to the condition that the ticket shall be cancelled online or online TDR shall be filed for all the passengers")
    pdf.set_xy(5,np(282+(x*y)))
    pdf.cell(0,4, txt = "upto thirty minutes before the scheduled departure of the train. ")
    pdf.set_xy(5,np(286+(x*y)))
    pdf.cell(0,4, txt = "14. For Suvidha Train, only 50% refund is allowed in case of cancellation of Confirm/RAC tickets upto 6 hours before the scheduled departure of the train or preparation of chart whichever is earlier.")
    pdf.set_xy(5,np(290+(x*y)))
    pdf.cell(0,4, txt = "15. In case of Train Cancellation, full refund will be granted automatically by the System.")
    pdf.set_xy(5,np(294+(x*y)))
    pdf.cell(0,4, txt = "16. Passengers are advised not to carry inflammable/dangerous/explosive/articles as part of their luggage and also to desist from smoking in the trains.")
    pdf.set_xy(5,np(298+(x*y)))
    pdf.cell(0,4, txt = "17. Contact us on:- 24*7 Hrs Customer Support at 011-23340000/011-39340000, Chennai Customer Care 044 - 25300000 or Mail To: care@irctc.co.in.")
    pdf.set_xy(5,np(302+(x*y)))
    pdf.cell(0,4, txt = "18. Variety of meals available in more than 1500 trains. For delivery of meal of your choice on your seat log on to www.ecatering.irctc.co.in or call")
    pdf.set_xy(5,np(306+(x*y)))
    pdf.cell(0,4, txt = "19. FOR MEDICAL EMERGENCY /FIRST AID, CONTACT TICKET CHECKING STAFF /GUARD OR DIAL 138.(ALL India Passenger Helpline No.138)")
    pdf.set_xy(5,np(310+(x*y)))
    pdf.cell(0,4, txt = "20. PNR and train arrival /departure enquiry no.139")
    pdf.set_xy(5,np(314+(x*y)))
    pdf.cell(0,4, txt = "21. To report unsavory situation during journey, Please dial railway security helpline no.182")
    pdf.set_xy(5,np(318+(x*y)))
    pdf.cell(0,4, txt = "22. All the Terms and conditions specified will be applicable in case of opting Travel Insurance facility. Please Refer Travel Insurance's Terms & Conditions available on Home page of")
    pdf.set_xy(5,np(321+(x*y)))
    pdf.cell(0,4, txt = "www.irctc.co.in website")
    pdf.set_xy(5,np(325+(x*y)))
    pdf.cell(0,4, txt = "23. Never purchase e-ticket from unauthorized agents or persons using their personal IDs for commercial purposes. Such tickets are liable to be can celled and forfeited without any refund of")
    pdf.set_xy(5,np(328+(x*y)))
    pdf.cell(0,4, txt = "money, under section (143) of the Indian Railway Act 1989. List of authorized agents are available on www.irctc.com E -Ticket Agent Locator.")
    pdf.output("static/ticket.pdf") 
    if int(passenger)==1:
        passenger= "1 Passenger"
    else:
       passenger=str(passenger)+" Passengers"
    return render_template('ticketsuccess.html',trainnamez=trainnamez,deptm=deptm,destm=destm,trainno=trainno,age=age,fname=fname,space=" ",price=fare,pnr=pnr,depst=depst,desst=desst,time=time,class1=class1,passenger=passenger,seat1=seat1,seat2=seat2,seat3=seat3,seat4=seat4,seat5=seat5,coach=coach,)

@app.route("/train-ticket/trainname=<trainnamez>trainno=<trainno>fullname=<fname>age=<age>gender=<gender>berth=<berth>depst=<depst>desst=<desst>time=<time>deptm=<deptm>destm=<destm>class=<class1>date=<date>mno=<mno>add=<add>")
def ticketbooking2(trainnamez,trainno,gender,fname,age,berth,depst,desst,time,deptm,destm,class1,date,mno,add):
    return render_template('booktrain2.html',trainnamez=trainnamez,deptm=deptm,destm=destm,trainno=trainno,age=age,fname=fname,space=" ",depst=depst,desst=desst,time=time,class1=class1,i=2)

@app.route("/train-ticket/trainname=<trainnamez>trainno=<trainno>fullname=<fname>age=<age>gender=<gender>berth=<berth>depst=<depst>desst=<desst>time=<time>deptm=<deptm>destm=<destm>class=<class1>date=<date>mno=<mno>add=<add>name2=<name2>age2=<age2>gender2=<gender2>berth2=<berth2>")
def ticketbooking3(trainnamez,trainno,gender,fname,age,berth,depst,desst,time,deptm,destm,class1,date,name2,age2,gender2,berth2,mno,add):
    return render_template('booktrain2.html',trainnamez=trainnamez,deptm=deptm,destm=destm,trainno=trainno,age=age,fname=fname,space=" ",depst=depst,desst=desst,time=time,class1=class1,i=3)

@app.route("/train-ticket/trainname=<trainnamez>trainno=<trainno>fullname=<fname>age=<age>gender=<gender>berth=<berth>depst=<depst>desst=<desst>time=<time>deptm=<deptm>destm=<destm>class=<class1>date=<date>mno=<mno>add=<add>name2=<name2>age2=<age2>gender2=<gender2>berth2=<berth2>name3=<name3>age3=<age3>gender3=<gender3>berth3=<berth3>")
def ticketbooking4(trainnamez,trainno,gender,fname,age,berth,depst,desst,time,deptm,destm,class1,date,name2,age2,gender2,berth2,name3,age3,gender3,berth3,mno,add):
    return render_template('booktrain2.html',trainnamez=trainnamez,deptm=deptm,destm=destm,trainno=trainno,age=age,fname=fname,space=" ",depst=depst,desst=desst,time=time,class1=class1,i=4)

@app.route("/train-ticket/trainname=<trainnamez>trainno=<trainno>fullname=<fname>age=<age>gender=<gender>berth=<berth>depst=<depst>desst=<desst>time=<time>deptm=<deptm>destm=<destm>class=<class1>date=<date>mno=<mno>add=<add>name2=<name2>age2=<age2>gender2=<gender2>berth2=<berth2>name3=<name3>age3=<age3>gender3=<gender3>berth3=<berth3>name4=<name4>age4=<age4>gender4=<gender4>berth4=<berth4>")
def ticketbooking5(trainnamez,trainno,gender,fname,age,berth,depst,desst,time,deptm,destm,class1,date,name2,age2,gender2,berth2,name3,age3,gender3,berth3,name4,age4,gender4,berth4,mno,add):
    return render_template('booktrain2.html',trainnamez=trainnamez,deptm=deptm,destm=destm,trainno=trainno,age=age,fname=fname,space=" ",depst=depst,desst=desst,time=time,class1=class1,i=5)

@app.route("/bored")
def bored():
    return render_template("areyoubored.html")

if __name__== "__main__":
    app.run(debug=True)