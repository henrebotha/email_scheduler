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
    settings = []
    with open("settings_account.cfg", "r") as f:
        for line in f:
            settings.append(line.strip().split(" = ")[1])
    return settings

def load_program_settings():
    settings = []
    with open("settings_program.cfg", "r") as f:
        for line in f:
            settings.append(line.strip().split(" = ")[1])
    return settings

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

account_settings = load_account_settings()
user = account_settings[0]
host = account_settings[1]
port = int(account_settings[2])

program_settings = load_program_settings()
debug = int(program_settings[0])
maildir = program_settings[1]
archdir = program_settings[2]
update_frequency = int(program_settings[3])

settings_display = [("User", user), ("Host", host), ("Port", port),
("Debug messages", "on" if debug == 1 else "off"), ("Email directory", maildir),
("Archive directory", archdir), ("Update frequency", update_frequency)]

for i in settings_display:
    print("{0:20}{1}".format(str(i[0]), str(i[1])))

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
