#conversions
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
def addcomma(f):
    f="'"+f+"'"
    return f  

#main functions
def coach():
    global coach
    coach=input('ENTER YOUR (1AC/2AC/3AC/2S/SL): ')
    if coach!='A1'or'A2'or'A3'or'S1'or'S2'or'S3':
        print('ENTER A VALID COACH')
        coach()

def time(h1,h2,m1,m2,t):
    print(t)
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

def mainmenu():
    print("1.SEARCH TRAIN")
    print("2.TRAIN DIRECTORY")
    ch=int(input("YOUR CHOICE: "))

    if ch == 1:
        searchtrain()
    elif ch == 2:
        traindirectory()
        
def findDay(date):
    import datetime
    import calendar
    d = datetime.datetime.strptime(date, '%d-%m-%Y').weekday()
    return (calendar.day_name[d])

def coach():
    global co
    co=input('ENTER YOUR CODE(A1/A2/A3/S1/S2/S3): ')
    if co=='A1'or co=='A2'or co=='A3'or co=='S1'or co=='S2'or co=='S3':
        pass
    else:
        print('ENTER A VALID COACH')
        coach()
        

def choosetr():
    global tr_no
    tr_no=int(input('ENTER THE TRAIN YOU WANT TO BOOK(TRAIN NO): '))
    for i in list_trains:
        if tr_no==(i):
            break
    else:
        print("CHOOSE A CORRECT TRAIN NUMBER")                 
        print(list_trains)
        choosetr()

def trainname(tn):
    mycursor.execute(f'select train_name from ts where train_no={tn}')
    output= mycursor.fetchall()
    global train_name
    train_name=converttuple(output)
    train_name=convertstring(train_name)
    return(train_name)

def dep(tn,dep_str):
    mycursor.execute(f'select hour from matrix where train_no={tn} AND value like {dep_str}')
    h1= mycursor.fetchall()
    h1=converttuple(h1)
    h1=convertint(h1)
    mycursor.execute(f'select minute from matrix where train_no={tn} AND value like {dep_str}')
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
    mycursor.execute(f'select value from matrix where train_no={tn} AND value like {dep_str}')
    output = mycursor.fetchall()
    global departure_station
    departure_station=converttuple(output)
    departure_station=convertstring(departure_station)
    return(H1+":"+M1+" "+departure_station)

def dest(tn,dest_str):
    mycursor.execute(f'select hour from matrix where train_no={tn} AND value like {dest_str}')
    h2 = mycursor.fetchall()
    h2=converttuple(h2)
    h2=convertint(h2)
    mycursor.execute(f'select minute from matrix where train_no={tn} AND value like {dest_str}')
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
    mycursor.execute(f'select value from matrix where train_no={tn} AND value like {dest_str}')
    output = mycursor.fetchall()
    global destination_station
    destination_station=converttuple(output)
    destination_station=convertstring(destination_station)
    return(H2+":"+M2+" "+destination_station)

def searchtrain():
    print("WELCOME TO OUR SEARCH ENGINE")
    departure=input("FROM: ")
    destination=input("TO: ")
    global date,day1
    date=input("DATE(DD-MM-YYYY): ")
    day1=str(findDay(date))
    day=day1[:2]
    day=("'%"+day+"%'")
    dep_str=("'%"+ departure + "%'")
    dest_str=("'%"+ destination + "%'")
    mycursor.execute(f'select train_no from ts where (s1 like {dep_str} or s2 like {dep_str} or s3 like {dep_str} or s4 like {dep_str} or s5 like {dep_str} or s6 like {dep_str} or s7 like {dep_str} or s8 like {dep_str} or s9 like {dep_str} or s10 like {dep_str} or s11 like {dep_str} or s12 like {dep_str} or s13 like {dep_str} or s14 like {dep_str} or s15 like {dep_str}) AND (s1 like {dest_str} or s2 like {dest_str} or s3 like {dest_str} or s4 like {dest_str} or s5 like {dest_str} or s6 like {dest_str} or s7 like {dest_str} or s8 like {dest_str} or s9 like {dest_str} or s10 like {dest_str} or s11 like {dest_str} or s12 like {dest_str} or s13 like {dest_str} or s14 like {dest_str} or s15 like {dest_str}) AND (DAYS like {day} or DAYS="DAILY")')
    output= mycursor.fetchall()
    train_no=converttuple(output)
    l=[]
    for tn in train_no:
        mycursor.execute(f'select col from matrix where train_no={tn} and (value like {dep_str})')
        output = mycursor.fetchall()
        departure_list=converttuple(output)
        mycursor.execute(f'select col from matrix where train_no={tn} and (value like {dest_str})')
        output= mycursor.fetchall()
        destination_list=converttuple(output)
        if departure_list < destination_list:
            tn=(str(tn))
            if len(tn)==4:
                tn=("0"+ str(tn))
            print("_____\n"+tn+"||"+trainname(tn))
            l.append(int(tn))
            print(dep(tn,dep_str),"o--------------o",dest(tn,dest_str))
            mycursor.execute(f'select DAYS from ts where train_no={tn}')
            output=mycursor.fetchall()
            day=converttuple(output)
            day=convertstring(day)
            print("Time Duration: "+time(H1,H2,M1,M2,tn),'\n'+day,'\n')

    global list_trains
    list_trains=l
    if list_trains==[]:
        print("NO SUCH TRAINS ARE AVAILABLE ON "+ date)
        print('THANK YOU FOR USING OUR SERVICE')
        exit(0)
    
    q=input("DO YOU WANT TO BOOK TICKETS? Y/N ")
    if q=="y" or q=="Y":
        print("\nlist of trains: ",list_trains)
        choosetr()
        global f
        f=open("ticket.txt",'w')
        dep(tr_no,dep_str)
        dest(tr_no,dest_str)
        trainname(tr_no)
        leaving_time=H1+":"+M1
        arriving_time=H2+":"+M2
        pnr=random.randint(1111111111,9999999999)
        pnr=str(pnr)
        list1= ['JOURNEY CUM RESERVATION TICKET','\nPNR NO: '+pnr,'\n'+str(tr_no),' ',train_name,'\n',date,'  ',day1,'\n'+departure_station,'       ',leaving_time,'\n',destination_station,'      ',arriving_time,'\n'+time(H1,H2,M1,M2,tn)]
        f.writelines(list1)
        booktrain()
        


def booktrain():
    name=input('FULL NAME: ')
    age=int(input('AGE: '))
    coach()
    if 0<=age<=4:
        print('NO TICKETS REQUIRED FOR CHILDREN BELOW 4 YEARS')
        anotherticket()
        print('THANK YOU FOR USING OUR SERVICE')
        exit()
    gender=input("GENDER(M/F/O): ")
    list1= ['\n\nCoach: '+co,'\nseatno: '+str(random.randint(1,99)),'\nName: '+name,'\nGender: '+gender,'\nAge: '+str(age),]
    f.writelines(list1)
    anotherticket()
    
def anotherticket():
    a=input("DO YOU WANT TO BOOK ANOTHER TICKET? ")
    if a=='y':
        booktrain()
    if a!='y':
        f.close()
        print('------------------------------------------',"\nYOUR TICKET HAVE BEEN BOOKED",'\nKINDLY CHECK TICKET.TXT FILE IN YOUR PC')
        print('THANK YOU FOR USING OUR SERVICE')
        exit()

def traindirectory():
    print("WELCOME TO TRAIN DIRECOTORY")
    print("1.SEE LIST OF TRAINS")
    print("2.ENTER NEW TRAINS")
    num=int(input("YOUR CHOICE: "))
    if num ==1:
        trainlist()
        x=input("GO BACK TO MAIN MENU(Y/N): ")
        if x=="y" or x=="Y":
            mainmenu()
        if x=="n" or "N":
            traindirectory()
            
    elif num ==2:
        inserttrain()
        x=input("DO YOU WANT TO CONTINUE?(Y/N): ")
        if x =="Y" or x=="y":
            inserttrain()
        if x=="n" or "N":
            mainmenu()
def u(x):
    mycursor.execute(f'select train_no from ts')
    output = mycursor.fetchall()
    train_list=converttuple(output)
    for y in list(train_list):
        if x==int(y):
            print('THIS TRAIN ALREADY EXISTS')
            inserttrain()

def inserttrain():
    train_no=int(input("TRAIN NO: "))
    u(train_no)
    train_name= input("TRAIN NAME: ")
    
    for i in range(1,16):
        s="s"
        t=(str(s)+str(i))
        globals()[t]=k=input("STATION "+str(i)+": ")
        if k=="":
            I=input('You are entering an empty space? y/n ')
            if I=="y" or I=="Y":
                q=str(i)
                break
            elif I=="n" or I=="N":
                globals()[t]=input("STATION "+str(i)+": ")
    train_name=addcomma(train_name).upper()
    S1=addcomma(s1).upper()
    S2=addcomma(s2).upper()
    S3=addcomma(s3).upper()
    S4=addcomma(s4).upper()
    S5=addcomma(s5).upper()
    S6=addcomma(s6).upper()
    S7=addcomma(s7).upper()
    S8=addcomma(s8).upper()
    S9=addcomma(s9).upper()
    S10=addcomma(s10).upper()
    S11=addcomma(s11).upper()
    S12=addcomma(s12).upper()
    S13=addcomma(s13).upper()
    S14=addcomma(s14).upper()
    S15=addcomma(s15).upper()

    day=input("DAYS: ")
    if day=="":
        day=input("DAYS: ").capitalize()
    day=addcomma(day)


    mycursor.execute(f'insert into ts values({train_no},{train_name},{S1},{S2},{S3},{S4},{S5},{S6},{S7},{S8},{S9},{S10},{S11},{S12},{S13},{S14},{S15},{day});')
    for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
        print("_")
        if i==int(q):
            break
        hour=input("HH"+str(i)+": ")
        
        minute=int(input("MM"+str(i)+": "))
        mycursor.execute(f'select s{i} from ts where train_no={train_no}')
        output = mycursor.fetchone()
        station = convertstring(output)
        station= addcomma(station)
        pk=(str(train_no)+str(i))
        pk=addcomma(pk)
        mycursor.execute(f'insert into matrix values({pk},{train_no}, {i}, {station},{hour},{minute});')
    mydb.commit()
    print(train_name,"HAS BEEN INSERTED INTO DIRECTORY")

def trainlist():
    global tn
    mycursor.execute(f'select train_name from ts')
    output = mycursor.fetchall()
    train_list=converttuple(output)
    for tn in train_list:
        print(tn)

#maincode
import mysql.connector
mydb= mysql.connector.connect(host="localhost",user="sqluser",passwd="password",database="rrs")
import random
mycursor= mydb.cursor()
mycursor.execute(f'select train_name from ts')
output = mycursor.fetchall()
train_list=converttuple(output)

s="‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ RAILWAY RESERVATION SYSTEM ___"
n=list(s.split(' '))
for t in n:
    gh=' '
    ab=len(t)//2
    f=20-ab
    print(str(f*gh)+t,)
global s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15
s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15='','','','','','','','','','','','','','',''
mainmenu()
print('THANK YOU FOR USING OUR SERVICE')