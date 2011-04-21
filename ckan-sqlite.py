#!/usr/bin/env python

from builder_ckan import builder as b

b.run('Emptying database...', 
      '/home/buildslave/drop-all-tables.sh %(ckan_instance_name)s buildslave localhost')

assert b.env['build_dir'].startswith('/home/buildslave/ckan/build') # double check
b.run('Emptying build folder...',
      'rm -rf %(build_dir)s/*')

b.run('Getting fabfile from...',
      'wget -O fabfile.py %(ckan_repo)s/default/fabfile.py')

b.run('Running fabfile...',
      'fab config_local:%(build_dir)s,%(ckan_instance_name)s,db_host=localhost,db_pass=biomaik15,no_sudo=True,skip_setup_db=True,revision=default deploy')

# Doesn't work - problem with subversion repo format.
#b.run('Versions of code...',
#      'pip -E %(pyenv_dir)s freeze')

b.run('Copying config for running nosetests...',
      'cp %(build_dir)s/%(ckan_instance_name)s/%(ckan_instance_name)s.ini %(src_dir)s/ckan/development.ini')

b.run('Quick tests...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test.ini')
