#!/usr/bin/env python

def system(cmd, is_verbose=True):
    import commands
    import sys
    import os
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

import os
cwd = os.getcwd()
assert cwd == '/home/buildslave/okfn/full/build'

release = 'ckan-1.3'
print "### Release: %r" % release

print "\n### Emptying database..."
cmd = "/home/buildslave/drop-all-tables.sh buildandsmoke buildslave localhost"
system(cmd)

print "\n### Emptying build folder..."
cmd = "rm -rf /home/buildslave/okfn/full/build/*"
system(cmd)

print "\n### Getting fabfile from..."
cmd = 'wget -O fabfile.py https://bitbucket.org/okfn/ckan/raw/default/fabfile.py'
system(cmd)

print "\n### Running fabfile..."
cmd = ". /home/buildslave/ve/bin/activate; /home/buildslave/ve/bin/fab config_local:/home/buildslave/okfn/full/build/,buildandsmoke,db_host=localhost,db_pass=biomaik15,no_sudo=True,skip_setup_db=True deploy"
system(cmd)

print "\n### Switching to release %r..." % release
cmd = "hg -R /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan up %s" % release
system(cmd)

print "\n### Copying config for running nosetests..."
cmd = "cp /home/buildslave/okfn/full/build/buildandsmoke/buildandsmoke.ini /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/development.ini"
system(cmd)

print "\n### Full tests using postgres..."
cmd = ". /home/buildslave/okfn/full/build/buildandsmoke/pyenv/bin/activate; /home/buildslave/okfn/full/build/buildandsmoke/pyenv/bin/nosetests -v --with-coverage --cover-package=ckan. /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/ckan/tests/ --ckan --with-pylons=/home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/test-core.ini"
system(cmd)

