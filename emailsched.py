#current issues:

#any mail will be sent late by up to update_frequency seconds. So keep this
#value realistic. update_frequency = 3600, for instance, will make your mails
#send up to an hour late. 

import smtplib #for sending mail
import time #for pausing execution using sleep()
import datetime #for scheduling dates
import os #for reading mails
import getpass

mail = {} #key: filename; value: tuple: datetime, from, to, subject, body

def add_mail():
    '''scan emails folder for new/updated emails'''
    print("Adding mail...")
    for fn in os.listdir(maildir):
        with open(maildir + "\\" + fn, "r") as f:
            mail[fn] = (get_date(f.readline()), f.readline().strip(),
                f.readline().strip(), f.readline().strip(), f.read())
    print(str(len(mail)) + " mail(s) queued")

def archive_mail(fn):
    '''move sent mails to archdir'''
    path_src = str(maildir + "\\" + fn)
    path_dest = str(archdir + "\\" + fn)
    try:
        os.rename(path_src, path_dest)
    except FileExistsError:
        #append _001 after the filename (before the extension, if there is one)
        #if that doesn't work, try successively bigger appends
        #if we get all the way to _999 and that doesn't work, just overwrite
        #the original filename
        for i in range(1,1000):
            fna = fn.split(".")
            fna[0] = fna[0] + "_" + "{0:03d}".format(i) #fna = filename adjusted
            if len(fna) == 1:
                fna = fna[0]
            else:
                fna = fna[0] + "." + fna[1]
            path_dest = str(archdir + "\\" + fna)
            try:
                os.rename(path_src, path_dest)
                break
            except FileExistsError:
                continue
        else:
            path_dest = str(archdir + "\\" + fn)
            os.remove(path_dest)
            os.rename(path_src, path_dest)

def check_schedule():
    '''see if current time matches a scheduled time'''
    if len(mail) == 0:
        return
    to_send = []
    for k, v in mail.items():
        delta = datetime.datetime.now() - v[0]
        if delta.seconds > 0 and delta.days >= 0:
            to_send.append(k)
    if len(to_send) > 0:
        send_mail(to_send)

def clear_old_mail():
    '''remove queued mails that no longer point to a valid file'''
    del_list = []
    for fn in mail:
        if fn not in os.listdir(maildir):
            del_list.append(fn)
    for fn in del_list:
        del mail[fn]

def configure_account():
    user = input("Please enter your email account username: ")
    
    host = input("Please enter your email host address: ")
    
    while True:
        try:
            port = int(input("Please enter the email host port: "))
            break
        except:
            print("Invalid input.")
    
    with open("settings_account.cfg", "w") as f:
        f.write("user = " + user + "\n")
        f.write("host = " + host + "\n")
        f.write("port = " + str(port) + "\n")

def configure_program():
    while True:
        try:
            debug = int(input("Type 1 if you want debug messages, or 0 otherwise: "))
            if debug != 0 and debug != 1:
                print("Invalid input.")
                continue
            break
        except:
            print("Invalid input.")
    
    maildir = input("Please enter path to mail (leave blank for default): ")
    if maildir == "":
        maildir = ".\\emails"
    
    archdir = input("Please enter path to archive (leave blank for default): ")
    if archdir == "":
        archdir = ".\\archive"
    
    while True:
        try:
            update = int(input("Please enter update frequency in seconds: "))
            break
        except:
            print("Invalid input.")
    
    with open("settings_program.cfg", "w") as f:
        f.write("debug = " + str(debug) + "\n")
        f.write("maildir = " + str(maildir) + "\n")
        f.write("archdir = " + str(archdir) + "\n")
        f.write("update = " + str(update) + "\n")
    
    os.makedirs(maildir, exist_ok=True)
    os.makedirs(archdir, exist_ok=True)

def display_settings():
    settings_display = [("User", user), ("Host", host), ("Port", port),
    ("Debug messages", "on" if debug == 1 else "off"),
    ("Email directory", maildir), ("Archive directory", archdir),
    ("Update frequency", update_frequency)]

    for i in settings_display:
        print("{0:20}{1}".format(str(i[0]), str(i[1])))
    print()

def email_scheduler():
    while True:
        password = get_password()
        try:
            test_password(password)
            print("Password accepted.")
            break
        except smtplib.SMTPAuthenticationError:
            print("Invalid password.")
    
    while True:
        add_mail()
        clear_old_mail()
        check_schedule()
        time.sleep(update_frequency)

def format_mail(mail_raw):
    '''convert mail data into format suitable for sending'''
    msg = "From: " + mail_raw[1] + "\n"
    #msg = msg + "To : " + mail_raw[2] + "\n"
    msg = msg + "Subject: " + mail_raw[3] + "\n"
    msg = msg + "\n" + mail_raw[4]
    return msg

def get_date(d):
    '''convert string from file into datetime object'''
    d = d.split(", ")
    d = [int(i) for i in d]
    d = datetime.datetime(d[0], d[1], d[2], d[3], d[4])
    return d

def get_password():
    password = getpass.getpass("Please enter your email password: ")
    return password

def load_account_settings():
    global user, host, port
    settings = []
    with open("settings_account.cfg", "r") as f:
        for line in f:
            settings.append(line.strip().split(" = ")[1])
    user = settings[0]
    host = settings[1]
    port = int(settings[2])

def load_program_settings():
    global debug, maildir, archdir, update_frequency
    settings = []
    with open("settings_program.cfg", "r") as f:
        for line in f:
            settings.append(line.strip().split(" = ")[1])
    debug = int(settings[0])
    maildir = settings[1]
    archdir = settings[2]
    update_frequency = int(settings[3])

def main_menu():
    print("1. Run email scheduler")
    print("2. Configure email account settings")
    print("3. Configure program settings\n")
    while True:
        try:
            choice = int(input("Please enter your choice: "))
        except:
            choice = 0
        print()
        if choice == 1:
            email_scheduler()
            break
        elif choice == 2:
            configure_account()
            load_account_settings()
            display_settings()
            break
        elif choice == 3:
            configure_program()
            load_program_settings()
            display_settings()
            break
        else:
            print("Invalid input.")

def send_mail(to_send):
    '''log in and send messages'''
    with smtplib.SMTP_SSL(host=host, port=port) as server:
        server.login(user, password)
        server.set_debuglevel(debug)
        for fn in to_send:
            print("Now sending " + fn)
            msg = format_mail(mail[fn])
            server.sendmail(mail[fn][1], mail[fn][2], msg)
    for fn in to_send:
        archive_mail(fn)

def test_password(password):
    with smtplib.SMTP_SSL(host=host, port=port) as server:
        server.login(user, password)

#-------------------------------------------------------------------------------
#MAIN LOOP
#-------------------------------------------------------------------------------

try:
    with open("settings_program.cfg"):
        pass
except IOError:
    configure_program()

try:
    with open("settings_account.cfg"):
        pass
except IOError:
    configure_account()

load_program_settings()
load_account_settings()
display_settings()

while True:
    main_menu()
