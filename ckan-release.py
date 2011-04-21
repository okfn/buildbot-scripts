#!/usr/bin/env python

from builder_ckan import builder as b

# Find the latest release branch
from mercurial import ui, hg
#repo = hg.repository(ui.ui(), '%(src_dir)s/ckan' % b.env)
repo = hg.repository(ui.ui(), 'https://bitbucket.org/okfn/ckan')
latest_release_branch = sorted([branch for branch in repo.branchmap() if branch.startswith('release-')])[-1]
print '## RELEASE BRANCH: %s\n' % latest_release_branch
b.env['revision'] = latest_release_branch

b.run('Emptying database...', 
      '/home/buildslave/drop-all-tables.sh %(ckan_instance_name)s buildslave localhost')

assert b.env['build_dir'].startswith('/home/buildslave/ckan/build') # double check
b.run('Emptying build folder...',
      'rm -rf %(build_dir)s/*')

b.run('Getting fabfile from...',
      'wget -O fabfile.py %(ckan_repo)s/default/fabfile.py')

b.run('Running fabfile...',
      'fab config_local:%(build_dir)s,%(ckan_instance_name)s,db_host=localhost,db_pass=biomaik15,no_sudo=True,skip_setup_db=True,revision=%(revision)s deploy')

b.run('Copying config for running nosetests...',
      'cp %(build_dir)s/%(ckan_instance_name)s/%(ckan_instance_name)s.ini %(src_dir)s/ckan/development.ini')

b.run('Quick tests...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test.ini')

#b.run('Full tests with postgres...',
#      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini')

