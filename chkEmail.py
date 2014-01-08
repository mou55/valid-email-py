#Author: neo1981
#Aim: Check valid email addresses

import smtplib
import sys
import os

if len(sys.argv) < 2 :
    print "Use: "+sys.argv[0]+" EmailsFile"
    exit(1)
validFile = "validemails.txt"
maildomain="gmail.com"
nsToken = "mail exchanger = "
mailserver = ""
print "Checking for MX Mailserver..."
plines = os.popen("nslookup -type=MX "+maildomain).readlines()
for pline in plines:
    if nsToken in pline:
        mailserver = pline.split(nsToken)[1].strip()
        break
    
if mailserver == "":
    print "Unable to get MX address for gmail.com"
    exit(1)
else:
    print "Found mailserver MX:",mailserver
f=open(sys.argv[1],"r")
lines = f.readlines()
f.close()
fvalid=open(validFile,"w")
for line in lines:
    email = line.strip()
    print "Checking email address:",email
    s = smtplib.SMTP(mailserver)
    rep1= s.ehlo()
    if rep1[0]==250 :     #250 denotes OK reply
        rep2=s.mail("test@rediff.com")
        if rep2[0]==250:
            rep3 = s.rcpt(email)
        if rep3[0] == 250:
            print email," is valid"
            fvalid.write(email+"\n") #email valid
        #elif rep3[0] == 550: #email invalid
fvalid.close()
print "Find valid emails in file:",validFile
