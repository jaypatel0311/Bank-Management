import sqlite3

db=sqlite3.connect('database.db')
cur=db.cursor()

cur.execute('CREATE TABLE Customer(customer_id number(16) primary key,full_name varchar2(50),gender varchar(1),address varchar2(100),city varchar2(20),state varchar2(20),pincode number(6))')
print("Customer Table Created Successfully...\n")

cur.execute('CREATE TABLE Account(account_no number(16) primary key,customer_id number(16),password varchar2(50),type varchar2(1),balance number(10),withdrawl_count number(2),last_date date,closure_date date)')
print("Account Table Created Successfully...\n")

cur.execute('CREATE TABLE Transactions(transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,account_no number(16),type varchar2(1),transaction_time date,balance number(10),amount number(10))')
print("Transaction Table Created Successfully...\n")

db.close()
