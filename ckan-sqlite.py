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

print "\n### Copying config for running nosetests..."
cmd = "cp /home/buildslave/okfn/full/build/buildandsmoke/buildandsmoke.ini /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/development.ini"
system(cmd)
#cmd = "mkdir /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/data || echo ''"
#system(cmd)
#cmd = "touch /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/data/who_log.ini"
#system(cmd)

print "\n### Quick tests..."
cmd = ". /home/buildslave/okfn/full/build/buildandsmoke/pyenv/bin/activate; /home/buildslave/okfn/full/build/buildandsmoke/pyenv/bin/nosetests -v /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/ckan/tests/ --ckan --with-pylons=/home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/test.ini"
system(cmd)

#print "Preparing for full tests..."
#cmd = "sed -i 's/\(faster_db_test_hacks.*\)/#\1/g' /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/test.ini"
#system(cmd)
#cmd = "sed -i 's/\(sqlalchemy.url.*\)/#\1/g' /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/test.ini"
#system(cmd)

#print "\n### Full tests..."
#cmd = ". /home/buildslave/okfn/full/build/buildandsmoke/pyenv/bin/activate; /home/buildslave/okfn/full/build/buildandsmoke/pyenv/bin/nosetests -v --with-coverage --cover-package=ckan. /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/ckan/tests/ --ckan --with-pylons=/home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/test-core.ini"
#system(cmd)

