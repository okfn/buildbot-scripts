from __future__ import with_statement
from fabric.api import abort, run, cd, sudo

def install_dgu_db():
    run("apt-get -y install postgresql")
    run("psql ...  -f .. ")

def setup_vm():
    # Comment out apt-proxy
    sudo("sed -i 's,Acquire::http { Proxy.*,// &,' /etc/apt/apt.conf")
    # Provide test apt server 
    sudo("echo 'deb http://apt.okfn.org/ubuntu_ckan-std_dev lucid universe' > /etc/apt/sources.list.d/okfn.list")
    sudo("wget -qO-  http://apt.okfn.org/packages.okfn.key | sudo apt-key add -")
    # Update and install required packages
    sudo("apt-get update")

def install_ckan():
    sudo("dpkg --configure -a") # needed on reinstall to tidy up
    sudo("apt-get update")
    sudo("apt-get -y --force-yes install ckan-std")
    #sudo("sed -i 's,ssl = true.*,ssl = false&,' /etc/postgresql/8.4/main/postgresql.conf") # turn off ssl to get postgres to install
