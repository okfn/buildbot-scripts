from __future__ import with_statement
from fabric.api import abort, run, cd, sudo, put
import os

def install_dgu_db():
    run("apt-get -y install postgresql")
    run("psql ...  -f .. ")

def setup_vm(instance='std'):
    # Copy on the database dump to be loaded
    dumps = sorted(os.listdir('/home/buildslave/dumps_gz'))
    sudo("mkdir -p /etc/ckan/dgu")
    put(
        os.path.join('/home/buildslave/dumps_gz', dumps[-1]), 
        '/tmp/latest.dump.gz',
    )
    sudo("mv /tmp/latest.dump.gz /etc/ckan/dgu/")
    sudo("gunzip /etc/ckan/dgu/latest.dump.gz")
    # Comment out apt-proxy
    sudo("sed -i 's,Acquire::http { Proxy.*,// &,' /etc/apt/apt.conf")
    # Provide test apt server 
    sudo("echo 'deb http://apt.okfn.org/ubuntu_ckan-%s_dev lucid universe' > /etc/apt/sources.list.d/okfn.list" % instance)
    sudo("wget -qO-  http://apt.okfn.org/packages.okfn.key | sudo apt-key add -")
    # Update and install required packages
    sudo("apt-get update")

def install_ckan(instance='std'):
    sudo("dpkg --configure -a") # needed on reinstall to tidy up
    sudo("apt-get update")
    sudo("apt-get -y --force-yes install ckan-%s" % instance)
    #sudo("sed -i 's,ssl = true.*,ssl = false&,' /etc/postgresql/8.4/main/postgresql.conf") # turn off ssl to get postgres to install
    sudo("ckan-%s-install" % instance)
