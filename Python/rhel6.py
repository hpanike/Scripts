#Base install for rhel6
# You should be able to run this script right after an install of RHEL 6 and
# expect the machine to be up and running.  Note that we expect a machine to
# be installed with "Minimal Install."

from subprocess import call as run
import sys, shlex, os, getpass, time

#random variables
AUTO=False
var=""

#check for automation
try:
     if sys.argv[1] == "auto" or sys.argv[2] == "auto":
	AUTO=True
except:
	IndexError
        print("Running manual")
# Package Lists:
BASE_PACKAGES="git openldap-clients zsh vim-enhanced ntp screen postfix pexpect expect"
DEV_PACKAGES="python-ldap MySQL-python gcc gcc-c++ autoconf automake"
CONFDIR="/git/serverconf"
LINK="ln -sf"

#NFS Fstab
NFS1 = 'echo "#nfs-home1:/home1        /users/home1    nfs4    auto,hard,intr,rw,suid,retrans=15,timeo=6           0       0" >>/etc/fstab'
NFS2 = 'echo "#nfs-home2:/home2        /users/home2    nfs4    auto,hard,intr,rw,suid,retrans=15,timeo=6           0       0" >>/etc/fstab'

if AUTO==False:
	print( "Before running this script, please make sure that the following has been done:")
	print(" - This machine has been added to DNS (both forward and reverse).")
	print( " - This machine has been added to git/serverconf/netgroup and nfs-network,")
	print( "     nfs-home1, and nfs-home2 have all been updated (including exportfs -a).")
	print("Also you may enable NFS mounts by running this script with the 'nfs-on' option or by entering it below")
	print(" ")
	print( "If any of this has not been done yet, please hit ^C.")
	print(" ")
	var = raw_input( "If all of this has been done, please hit Enter: ")

try:
	if var == "nfs-on" or sys.argv[1] == "nfs-on":
		NFS1 = 'echo "nfs-home1:/home1        /users/home1    nfs4    auto,hard,intr,rw,suid,retrans=15,timeo=6           0       0" >>/etc/fstab'
		NFS2 = 'echo "nfs-home2:/home2        /users/home2    nfs4    auto,hard,intr,rw,suid,retrans=15,timeo=6           0       0" >>/etc/fstab'
		print("Mounting NFS shares on reboot")
except:
	IndexError
	print("Not mounting NFS shares on boot")

if AUTO==False:
	password = getpass.getpass("Enter password for git.cs.byu.edu: ")
install = (
#register system
"rhnreg_ks --activationkey=74f34235c3e268faeec30448f61008ca --force",
#Update packages and install important packages
"wget -O /etc/yum.repos.d/rhel6-mirror.repo mirrors.cs.byu.edu/rhel/rhel6-mirror.repo",
"/usr/bin/yum -y upgrade",
"/usr/bin/yum -y install "+BASE_PACKAGES+" "+DEV_PACKAGES)

for i in install:
	run(shlex.split(i))
import pexpect
if AUTO==True:
	run(shlex.split("ssh -o 'StrictHostKeyChecking no' git.cs.byu.edu"))
	if os.path.isdir("/git/serverconf/") == False:
		run(shlex.split("git clone ssh://git.cs.byu.edu/etc/git/serverconf.git /git/serverconf/"))
        if os.path.isdir("/git/services/") == False:
		run(shlex.split("git clone ssh://git.cs.byu.edu/etc/git/services.git /git/services/"))
else:
	#git stuff, make sure folder doesn't exist. also need to install git before this
	ssh_newkey = 'Are you sure you want to continue connecting'
	if os.path.isdir("/git/serverconf/") == False:
		p=pexpect.spawn('git clone ssh://git.cs.byu.edu/etc/git/serverconf.git /git/serverconf/')
		i=p.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==0:
		    p.sendline('yes')
		    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==1:
		    p.sendline(password)
	   	    p.expect(pexpect.EOF)
		elif i==2:
	 	   print "connection timeout"
	 	   exit()
		print p.before

	if os.path.isdir("/git/services/") == False:
		p=pexpect.spawn('git clone ssh://git.cs.byu.edu/etc/git/services.git /git/services/')
		i=p.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==0:
		    p.sendline('yes')
		    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==1:
		    p.sendline(password)
		    p.expect(pexpect.EOF)
		elif i==2:
		    print "connection timeout"
		    exit()
		print p.before

#check to make sure something didn't go wrong
if os.path.isdir("/git/serverconf/etc/") == False:
	print("something went wrong with the git pull. make sure it /git/serverconf is present or the system will malfuntion")
	exit()


cmds= (
"mkdir -p /etc/openldap/cacerts",
# setup ldap, kerberos
LINK+" "+CONFDIR+"/cacerts/cacert.pem /etc/openldap/cacerts/",
LINK+" "+CONFDIR+"/etc/krb5.conf /etc/",
LINK+" "+CONFDIR+"/etc/krb.conf /etc/",
LINK+" "+CONFDIR+"/etc/ldap.conf /etc/",
LINK+" "+CONFDIR+"/etc/pam_ldap.conf /etc/",

# setup nslcd
# used rhel5 installer to help (nsswitch, krb, system auth, etc)
LINK+" "+CONFDIR+"/etc/nslcd.conf /etc/nslcd.conf",
LINK+" "+CONFDIR+"/etc/nsswitch.conf /etc/nsswitch.conf",
LINK+" "+CONFDIR+"/etc/pam.d/password-auth /etc/pam.d/password-auth",
LINK+" "+CONFDIR+"/etc/pam.d/system-auth /etc/pam.d/system-auth",

# Other config files
LINK+" "+CONFDIR+"/etc/netgroup /etc/",
LINK+" "+CONFDIR+"/etc/hosts.allow /etc/",
LINK+" "+CONFDIR+"/etc/hosts.deny /etc/",
LINK+" "+CONFDIR+"/etc/idmapd.conf /etc/",
LINK+" "+CONFDIR+"/etc/ntp.conf /etc/",
LINK+" "+CONFDIR+"/etc/ssh/sshd_config /etc/ssh/",
LINK+" "+CONFDIR+"/etc/yum.repos.d/rhel6-mirror.repo /etc/yum.repos.d/",

# Root's home directory
LINK+" "+CONFDIR+"/root/bashrc /root/.bashrc",

# Setup link for p-run
"ln -sf /usr/network/scripts/p-run /usr/local/bin/p-run",

# Setup smtp (postfix)
"sed -i '0,/^\(#relayhost\s=\s\$mydomain\)/s//relayhost = mail.cs.byu.edu/' /etc/postfix/main.cf",
# Turn on services
"chkconfig ntpdate on",
"chkconfig ntpd on",
"chkconfig nslcd on",
"chkconfig postfix on",
########################################################################
# Setup NFS mounts
"mkdir -p /users/home1",
"mkdir -p /users/home2",
NFS1,
NFS2,
# Create symlinks for groups
"ln -sf /users/home1/helpdesk /users/helpdesk",
"ln -sf /users/home1/faculty /users/faculty",
"ln -sf /users/home1/staff /users/staff",
"ln -sf /users/home1/guest /users/guest",
"ln -sf /users/home2/admin /users/admin",
"ln -sf /users/home2/ta /users/ta",
"ln -sf /users/home2/grads /users/grads",
"ln -sf /users/home2/ugrad /users/ugrad",
"ln -sf /users/home2/visitors /users/visitors",
"ln -sf /users/home2/groups /users/groups",
"ln -sf /users/home1/network /usr/network",

# Disable SELinux
"sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config"
)
for i in cmds:
	run(shlex.split(i))
#mir public key
f = open('/root/.ssh/authorized_keys', 'a')
keys = open(CONFDIR+"/root/backup.pub", 'r')
for line in keys:
	f.write(line)
f.close()
keys.close()

print("Rebooting the computer in 10 seconds.")
time.sleep(10)
run(['reboot'])
exit()

