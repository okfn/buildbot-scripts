#!/usr/bin/env python

from builder_ckanext import builder as b
b.env['revision'] = 'default'

b.run('Emptying database', 
      '/home/buildslave/drop-all-tables.sh %(ckan_instance_name)s buildslave localhost')

assert b.env['build_dir'].startswith('/home/buildslave/ckanext/build') # double check
b.run('Emptying build folder',
      'rm -rf %(build_dir)s/*')

b.run('Getting fabfile',
      'wget -O fabfile.py %(ckan_repo_files)s/master/fabfile.py')

b.run('Install CKAN with fabfile',
      'fab config_local:%(build_dir)s,%(ckan_instance_name)s,db_host=localhost,db_pass=biomaik15,no_sudo=True,skip_setup_db=True,revision=%(revision)s deploy')

b.run('Copying config for running nosetests',
      'cp %(build_dir)s/%(ckan_instance_name)s/%(ckan_instance_name)s.ini %(src_dir)s/ckan/development.ini')

b.run('Install ckanext-importlib',
      'pip -E %(pyenv_dir)s install -e git+http://github.com/okfn/ckanext-importlib#egg=ckanext-importlib')

b.run('Install ckanext-importlib dependencies',
      'pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-importlib/pip-requirements.txt')

b.run('Quick tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-importlib/ckanext/importlib/tests/ --ckan --with-pylons=%(src_dir)s/ckanext-importlib/test.ini')

b.run('Full tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-importlib/ckanext/importlib/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini')

