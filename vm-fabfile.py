from __future__ import with_statement
from fabric.api import abort, run, cd, sudo

def install_dgu_db():
    run("apt-get -y install postgresql")
    run("psql ...  -f .. ")

def setup_vm():
    # Comment out apt-proxy
    sudo("sed -i 's,Acquire::http { Proxy.*,// &,' /etc/apt/apt.conf")
    sudo("echo 'deb http://apt.okfn.org/ubuntu_ckan-test lucid universe' > /etc/apt/sources.list.d/okfn.list")

def install_ckan():
    sudo("apt-get update")
    sudo("apt-get install ckan")
