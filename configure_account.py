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
