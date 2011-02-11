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
pyenv = 'ckan-dgu-buildandsmoke/pyenv'
cmds = [
#('Installing ckanclient code', '%s/bin/pip -E %s install -e hg+http://bitbucket.org/okfn/ckanclient#egg=ckanclient' % (pyenv, pyenv)),
('Running ckanclient tests', '. %s/bin/activate && nosetests -v %s/src/ckanclient/ckanclient/tests/ --ckan --with-pylons=%s/src/ckanclient/test.ini' % (pyenv, pyenv, pyenv)),
]

for info, cmd in cmds:
    print '== %s ==' % info
    system(cmd)
    print


