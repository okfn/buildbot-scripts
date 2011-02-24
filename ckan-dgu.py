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
#('Emptying database', '/home/buildslave/drop-all-tables.sh ckan-dgu-buildandsmoke buildslave localhost'),
#('Emptying build folder', 'rm -rf /home/buildslave/okfn/dgu/build/*'),
#('Getting CKAN fabfile', 'wget -O fabfile.py http://knowledgeforge.net/ckan/hg/raw-file/default/fabfile.py'),
#('Installing CKAN with fabfile', '/home/buildslave/ve/bin/fab config_local:/home/buildslave/okfn/dgu/build/,ckan-dgu-buildandsmoke,db_host=localhost,db_pass=biomaik15,no_sudo=True,skip_setup_db=True deploy'),
#('Copy config to development.ini for tests', 'cp ckan-dgu-buildandsmoke/ckan-dgu-buildandsmoke.ini %s/src/ckan/development.ini' % pyenv),
('Installing dgu code', '%s/bin/pip -E %s install -e hg+http://bitbucket.org/okfn/ckanext-dgu#egg=ckanext-dgu' % (pyenv, pyenv)),
#('Installing ckanext code', '%s/bin/pip -E %s install -e hg+https://knowledgeforge.net/ckan/ckanext#egg=ckanext' % (pyenv, pyenv)),
#('Installing dgu (and deps)', '%s/bin/python dgu/setup.py develop' % pyenv),
#('Unlinking release of ckanclient', '%s/bin/pip -E %s uninstall ckanclient --yes' % (pyenv, pyenv)),
#('Wiping release of ckanclient', 'rm -rf /home/buildslave/okfn/dgu/build/%s/src/ckanclient' % pyenv),
#('Installing newest ckanclient code', '%s/bin/pip -E %s install -e hg+https://knowledgeforge.net/ckan/ckanclient#egg=ckanclient' % (pyenv, pyenv)),
#('Running ckanext tests', '%s/bin/nosetests -q --nologcapture %s/src/ckanext/ckanext/tests/' % (pyenv, pyenv)),
('Running dgu tests on Sqlite', '. %s/bin/activate && nosetests -v %s/src/ckanext-dgu/ckanext/dgu/tests/ --ckan --with-pylons=%s/src/ckanext-dgu/test.ini' % (pyenv, pyenv, pyenv)),
('Running dgu tests on Postgres', '. %s/bin/activate && nosetests -v %s/src/ckanext-dgu/ckanext/dgu/tests/ --ckan --with-pylons=%s/src/ckanext-dgu/test-core.ini' % (pyenv, pyenv, pyenv)),
]

for info, cmd in cmds:
    print '== %s ==' % info
    system(cmd)
    print


