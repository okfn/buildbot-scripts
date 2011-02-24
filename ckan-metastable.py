#!/usr/bin/env python

import os

def system(cmd, is_verbose=True):
    import commands
    import sys
    print cmd
    if is_verbose:
        if os.system(cmd):
            print "Error: Couldn't run command: %s" % (cmd)
            sys.exit(1)
    else:
        (status, output) = commands.getstatusoutput(cmd)
        if status:
            print output
            print "Error: Couldn't run command: %s" % (cmd)
            sys.exit(1)

module_name = 'ckan-metastable'
deploy_name = dbname = 'ckan-metastable-buildandsmoke'
build_dir = '/home/buildslave/okfn/%s/build/' % 'full'
ve_bin_dir = '/home/buildslave/ve/bin/'
pyenv_dir = os.path.join(build_dir, deploy_name, 'pyenv')
src_dir = os.path.join(pyenv_dir, 'src')

print "Emptying database..."
cmd = "/home/buildslave/drop-all-tables.sh %s buildslave localhost" % dbname
system(cmd)

print "Emptying build folder..."
assert build_dir.startswith('/home/buildslave/okfn/')
cmd = "rm -rf %s/*" % build_dir
system(cmd)

print "Getting fabfile..."
cmd = 'wget -O fabfile.py https://bitbucket.org/okfn/ckan/raw/default/fabfile.py'
system(cmd)

print "Deploying ckan with fabfile..."
cmd = "%s/fab config_local:%s,%s,db_host=localhost,db_pass=biomaik15,no_sudo=True,skip_setup_db=True,revision=metastable deploy" % (ve_bin_dir, build_dir, deploy_name)
system(cmd)

print "Installing config..."
cmd = "cp %s/%s/%s.ini %s/ckan/development.ini" % (build_dir, deploy_name, deploy_name, src_dir)
system(cmd)

print "Starting test suite... (please wait)"
cmd = ". %s/bin/activate; nosetests -v --ckan --with-pylons %s/ckan/test.ini %s/ckan/ckan/tests/" % (pyenv_dir, src_dir, src_dir)
system(cmd)


