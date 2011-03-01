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

pyenv = 'ckan-dgu-buildandsmoke/pyenv'
build_dir = '/home/buildslave/okfn/dgu/build/'
assert os.getcwd() + '/' == build_dir, os.getcwd()

cmds = [
('Emptying database', '/home/buildslave/drop-all-tables.sh ckan-dgu-buildandsmoke buildslave localhost'),
('Emptying build folder', 'rm -rf /home/buildslave/okfn/dgu/build/*'),
('Getting CKAN fabfile', 'wget -O fabfile.py https://bitbucket.org/okfn/ckan/raw/default/fabfile.py'),
('Installing CKAN with fabfile', '/home/buildslave/ve/bin/fab config_local:%s,ckan-dgu-buildandsmoke,db_host=localhost,db_pass=biomaik15,no_sudo=True,skip_setup_db=True,revision=default deploy' % build_dir),
('Copy config to development.ini for tests', 'cp ckan-dgu-buildandsmoke/ckan-dgu-buildandsmoke.ini %s/src/ckan/development.ini' % pyenv),
#('Installing dgu code', '%s/bin/pip -E %s install -e hg+https://knowledgeforge.net/ckan/dgu#egg=dgu' % (pyenv, pyenv)),
('Installing ckanext code', '%s/bin/pip -E %s install -e hg+https://bitbucket.org/okfn/ckanext#egg=ckanext' % (pyenv, pyenv)),
('Installing ckanext dependencies', '%s/bin/pip -E %s install -r %s/src/ckanext/pip-requirements.txt' % (pyenv, pyenv, pyenv)),
#('Installing dgu (and deps)', '%s/bin/python dgu/setup.py develop' % pyenv),
#('Unlinking release of ckanclient', '%s/bin/pip -E %s uninstall ckanclient --yes' % (pyenv, pyenv)),
#('Wiping release of ckanclient', 'rm -rf /home/buildslave/okfn/dgu/build/%s/src/ckanclient' % pyenv),
#('Installing newest ckanclient code', '%s/bin/pip -E %s install -e hg+https://knowledgeforge.net/ckan/ckanclient#egg=ckanclient' % (pyenv, pyenv)),
('Running ckanext tests on Sqlite', '%s/bin/nosetests -v %s/src/ckanext/ckanext/tests/ --ckan --with-pylons=%s/src/ckan/test.ini' % (pyenv, pyenv, pyenv)),
('Running ckanext tests', '%s/bin/nosetests -v %s/src/ckanext/ckanext/tests/ --ckan --with-pylons=%s/src/ckan/test-core.ini' % (pyenv, pyenv, pyenv)),
#('Running dgu tests', '%s/bin/nosetests -q --nologcapture %s/src/dgu/ckanext/dgu/tests/' % (pyenv, pyenv)),
]

for info, cmd in cmds:
    print '== %s ==' % info
    system(cmd)
    print


