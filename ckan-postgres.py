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

print "\n### Full tests using postgres..."
cmd = ". /home/buildslave/okfn/full/build/buildandsmoke/pyenv/bin/activate; /home/buildslave/okfn/full/build/buildandsmoke/pyenv/bin/nosetests -v --with-coverage --cover-package=ckan. /home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/ckan/tests/ --ckan --with-pylons=/home/buildslave/okfn/full/build/buildandsmoke/pyenv/src/ckan/test-core.ini"
system(cmd)

