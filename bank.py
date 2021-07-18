import datetime
import sqlite3

db=sqlite3.connect('database.db')
cur=db.cursor()

def login():
    for i in range(0,3):
        try:
            global acc
            acc= int(input("Enter your Account Number : "))
            password = input("Enter Password : ")
        except:
            continue
        try:
            a = cur.execute('SELECT password FROM Account WHERE account_no = :1 and closure_date is NULL',(acc,))
        except:
            print("Database error")
            continue
        a = cur.fetchall()
        if(a):
            a = a[0][0]
        
            if(a == password):
                loginpage()
                break
            else:
                print('Wrong password try again')
        else:
            print("Invalid Account Number")
def signin():
    for i in range(1,11):
            acc_type = input("\nSelect Account Type (s for saving account and c for current account) : ")
            amount = int(input("Amount initiated : "))
            if (acc_type is 'c' and amount < 5000) or (amount < 0):
                print("Invalid Amount")
                continue
            print("Enter your details:")
            name = input("\nFull Name : ")
            gender = input("\nGender (Enter m for male and f for female) : ")
            address = input("\nAddress : ")
            city = input("\nCity : ")
            state = input("\nState : ")
            try:
                pincode = int(input("\nPincode : "))
            except:
                print("Wrong input TryAgain")
                continue
            from random import randint
            rand=randint(1000,5000)
            cur.execute('INSERT INTO Customer VALUES(:0,:1,:2,:3,:4,:5,:6)',(rand,name,gender,address,city,state,pincode))

            db.commit()

            ano = cur.execute('SELECT customer_id FROM Customer where full_name = :1 and address = :2',(name,address))
            acn = cur.fetchall()
            acn = acn[0][0]

            password = input("Set Password : ")

            
        
            cur.execute('INSERT INTO Account VALUES(:0,:1,:2,:3,:4,0,:5,NULL)',(rand,acn,password,acc_type,amount,datetime.datetime.now()))

            db.commit()

            ano = cur.execute('SELECT account_no FROM Account where customer_id = :1 and password = :2',(acn,password)).fetchall()
            acn = ano[0][0]

            print ("\nYour Account number : ",acn)

            break
       
def loginpage():
    cus_id = cur.execute('SELECT customer_id FROM Account WHERE account_no = :1',(acc,)).fetchall()
    cus_id = cus_id[0][0]
    for i in range(0,10):
        print("Choose Wisely\n\n1.Balance enquiry \n2. Address Change\n3. Money Deposit\n4. Money Withdrawal\n5. Transfer Money\n6. Account Closure\n7. View Profile\n0. Customer Logout")
        x = int(input("Enter your choice : "))
        if(x == 1):
            bal=cur.execute('SELECT balance from Account WHERE account_no=:1',(acc,)).fetchall()
            bal=bal[0][0]
            print("Your Current Balance is:",bal)
        elif(x == 2):
            #Changing Address
            address = input("Enter address : ")
            city = input("City : ")
            state = input("State : ")
            pincode = int(input("Pincode : "))
        
            cur.execute('UPDATE Customer SET address = :1, city = :2, state = :3, pincode = :4 WHERE customer_id = :5',(address,city,state,pincode,cus_id))
            print("Address successfully changed\n")
            db.commit()
        elif(x == 3):
            #Money Deposit
            amount = int(input("Enter Amount to be deposited : "))
            typet = 'd'
            bal = cur.execute('SELECT balance FROM Account WHERE account_no = :1',(acc,)).fetchall()
            bal = bal[0][0]
            bal = bal + amount
            print("Now your Balance is: ",bal)
            cur.execute('UPDATE Account SET balance = :1 WHERE account_no = :2',(bal,acc))
            db.commit()
        elif(x == 4):
            #Money Withdrawl
            amount = int(input("Enter Amount to be withdrawl : "))
            typet = 'w'
            bal = cur.execute('SELECT balance,type FROM Account WHERE account_no = :1',(acc,)).fetchall()
            acc_type = bal[0][1]
            bal = bal[0][0]
            if(acc_type is 'c' and (bal-amount) < 5000):
                print('Not enough balance')
                continue
            if(bal-amount < 0):
                print('Not enough balance')
                continue
            bal=bal-amount
            cur.execute('UPDATE Account SET balance = :1 WHERE account_no = :2',(bal,acc,))
            print("Now Your balance is :",bal)
            db.commit()
        elif(x == 5):
            #Transfer Money
            acc2 = int(input('Enter Account No. to transfer money : '))
            a = cur.execute('SELECT account_no,balance FROM Account WHERE account_no = :1',(acc2,))
            if(a):
                amount = int(input('Enter amount to Transfer : '))
                a = cur.fetchall()
                bal = a[0][1]
                my = cur.execute('SELECT balance,type FROM Account WHERE account_no = :1',(acc,)).fetchall()
                mytype = my[0][1]
                mybal = my[0][0]
                if(mytype is 'c' and (mybal-amount) < 5000):
                    print('Not enough balance')
                    continue
                if((mybal-amount) < 0):
                    print('Not enough balance')
                    continue
                mybal = mybal-amount
                #acc
                bal = bal + amount
                #acc2
                cur.execute('UPDATE Account SET balance = :1 WHERE account_no = :2',(mybal,acc))
                typet = 'w'
                
                cur.execute('UPDATE Account SET balance = :1 WHERE account_no = :2',(bal,acc2))
                typet = 'd'
                db.commit()
                print("Transfered Successfully")
            else:
                exit()
        elif(x == 6):
            #Account Closure
            print("ARE YOU SURE YOU WANT TO CLOSE YOUR ACCOUNT,for YES press Y :")
            s=input()
            if s is 'y' or 'Y':
                cur.execute('DELETE FROM Customer WHERE customer_id = :1',(cus_id,))
                cur.execute('DELETE FROM Account WHERE account_no = :1',(acc,))
                db.commit()
                print("Your Account is Successfully Closed")
        elif(x == 7):
            print("******************* YOUR PROFILE **************************\n")
            name=cur.execute('SELECT full_name FROM Customer WHERE customer_id= :1',(cus_id,)).fetchall()
            name=name[0][0]
            print("Hi, ",name)
            print("Your Account Number is ",acc)
            print("Your Customer Id is: ",cus_id) 
            date=cur.execute('SELECT last_date FROM Account WHERE account_no= :1',(acc,)).fetchall()
            date=date[0][0]
            print("Your Account created on ",date)
            acc_type=cur.execute('SELECT type FROM Account WHERE account_no= :1',(acc,)).fetchall()
            acc_type=acc_type[0][0]
            if acc_type is 's':
                print('Your account type is Saving Account')
            else:
                print('You account type is Current Account')
            add=cur.execute('SELECT address FROM Customer WHERE  customer_id= :1',(cus_id,)).fetchall()
            add=add[0][0]
            city=cur.execute('SELECT city FROM Customer WHERE  customer_id= :1',(cus_id,)).fetchall()
            city=city[0][0]
            state=cur.execute('SELECT state FROM Customer WHERE  customer_id= :1',(cus_id,)).fetchall()
            state=state[0][0]
            pin=cur.execute('SELECT pincode FROM Customer WHERE  customer_id= :1',(cus_id,)).fetchall()
            pin=pin[0][0]
            print('Your Address is : ',add,city,state,'Pincode: ',pin)
            bal = cur.execute('SELECT balance FROM Account WHERE account_no = :1',(acc,)).fetchall()
            bal = bal[0][0]
            print("Your Balance is :",bal)
            print("To change Password,press 1")
            a=int(input())
            if(a is 1):
                password=input("Enter New Pasword : ")
                cur.execute('UPDATE Account SET password = :1 WHERE account_no = :2',(password,acc))
                print("Password Changed Successfully")
            db.commit()
        elif(x is 0):
            #Logout
            print("You Logged Out Successfully")
            break
        else:
            print("Wrong Input Try Again")
            break
        
print("\t\t\tWelcome to Bank Of Spain Portal\t\t\t")
print("\n\nSelect Option")
print('1.Login to Your Account \n2. Don`t have account,Sign Up!!\n3.Exit')
n=int(input())
if n==1:
    login()
elif n==2:
    signin()
else:
    exit()

