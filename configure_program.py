import os

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
