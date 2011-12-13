#!/usr/bin/env python

from builder_ckanext import builder as b

b.run('Emptying database', 
      '/home/buildslave/drop-all-tables.sh %(ckan_instance_name)s buildslave localhost')

assert b.env['build_dir'].startswith('/home/buildslave/ckanext/build') # double check
b.run('Emptying build folder',
      'rm -rf %(build_dir)s/*')

b.run('Create pyenv',
      'virtualenv %(pyenv_dir)s')

b.run('Install ckanext-dgu',
      '%(pyenv_dir)s/bin/pip -E %(pyenv_dir)s install -e git+http://github.com/okfn/ckanext-dgu#egg=ckanext-dgu')

b.run('Install ckanext-dgu dependencies',
      '%(pyenv_dir)s/bin/pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-dgu/requires/lucid_missing.txt')

b.run('Install ckan dependencies',
      '%(pyenv_dir)s/bin/pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckan/pip-requirements.txt')

b.run('Install ckanext-harvest dependencies',
      '%(pyenv_dir)s/bin/pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-harvest/pip-requirements.txt')

b.run('Install ckanext-importlib dependencies (for dgu tests)',
      '%(pyenv_dir)s/bin/pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-importlib/pip-requirements.txt')

b.run('Install nose',
      '%(pyenv_dir)s/bin/pip -E %(pyenv_dir)s install nose')

b.run('Creating config for running nosetests...',
      '%(pyenv_dir)s/bin/paster make-config ckan %(src_dir)s/ckan/development.ini')

b.run('Editing config',
      'sed -e "s,^\(sqlalchemy.url\)[ =].*,\\1 = postgresql://buildslave:biomaik15@localhost/ckanext," -i %(src_dir)s/ckan/development.ini')

b.run('Quick tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-dgu/ckanext/dgu/tests/ --ckan --with-pylons=%(src_dir)s/ckanext-dgu/test.ini')

b.run('Full tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-dgu/ckanext/dgu/tests/ --ckan --with-pylons=%(src_dir)s/ckanext-dgu/test-core.ini')


