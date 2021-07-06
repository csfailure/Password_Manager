import sqlite3
import pandas as pd

ADMIN_PASSWORD = "123456"

user_password = input("What is your main password?\n")

while user_password != ADMIN_PASSWORD:
    user_password = input("What is your main password?\n")
    if user_password == "q":
        break


def create_password(service):
    pass1 = input("Enter the password for the given service: ")
    pass_copy = input("Confirm your new password: ")
    if pass1 == pass_copy:
        c.execute("INSERT INTO passwords VALUES (?,?)",(service,pass1))
        print("\n")
        print("*"*30)
        print("Password Created Successfully")
        print("*"*30)
        conn.commit()
    else:
        print("\n")
        print("!!!The passwords didn't match!!!")
        print("\n")
        create_password(service)
        
def show_passwords():
    print ("\n")
    print (pd.read_sql_query("SELECT * FROM passwords", conn))
        
def get_password(): 
    
    sth = True
    while sth:
        service = input("What is the name of the service? : ")
        c.execute("SELECT service FROM passwords WHERE service=(?)",(service,))
        service_exist = c.fetchall()
        if (len(service_exist) == 0 and service != "q"):
            print("There is no service named {}".format(service))
            print("\n")
            print("Enter again: ")
            continue
        
        elif service == "q":
            break
        
        else:
            p = c.execute("SELECT password FROM passwords WHERE service=(?)",(service,))
            print("*"*50)
            print("The password for {} is: {}".format(service, p.fetchone()[0]))
            print("*"*50)
            sth = False
            
def update_password(service):
    new_password = input("Enter new password: ")
    new_password_copy = input("Confirm new password: ")
    if new_password == new_password_copy:
        sql_update_pass = """UPDATE passwords SET password = (?) WHERE service = (?)"""
        updates = (new_password, service)
        c.execute(sql_update_pass, updates)
        conn.commit()
        print ("\n")
        print ("**Password successfully updated**")
    else:
        print("\n")
        print("!!!The passwords didn't match!!!")
        print("\n")

        update_password(service)
    
def delete_password(service):
    sql_delete_pass = "DELETE FROM passwords WHERE service=?"
    c.execute(sql_delete_pass, (service,))
    conn.commit()
          

if user_password == ADMIN_PASSWORD:
    
    conn = sqlite3.connect('pass_man.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS passwords (
                service text NOT NULL UNIQUE,
                password text)""")

    conn.commit()
    
    while True:
        print("\n"+ "*"*15)
        print("Commands:")
        print("q = quit program")
        print("gp = get password")
        print("cp = create password")
        print("sp = show passwords")
        print("up = update password")
        print("dp = delete password")
        print("*"*15)
        input_ = input(":")

        if input_ == "q":
            conn.close()
            break
        if input_ == "cp":
            service = input("What is the name of the service?: ")
            create_password(service)
            conn.commit()
        if input_ == "gp":
            get_password()
        if input_ ==  "sp":
            show_passwords()
        if input_ == "up":
            service = input("What is the name of the service?: ")
            update_password(service)
        if input_ == "dp":
            service = input("What is the name of the service?: ")
            delete_password(service)
            
