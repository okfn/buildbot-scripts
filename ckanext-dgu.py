#!/usr/bin/env python

from builder_ckanext import builder as b

b.run('Remove potential conflicts',
      'rm -rf %(pyenv_dir)s/src/ckanext-importlib %(pyenv_dir)s/src/ckanclient %(pyenv_dir)s/src/datautil')

b.run('Install ckanext-dgu',
      'pip -E %(pyenv_dir)s install -e hg+http://bitbucket.org/okfn/ckanext-dgu#egg=ckanext-dgu')

b.run('Install ckanext-dgu dependencies',
      'pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-dgu/pip-requirements.txt')

b.run('Install ckanext-harvest dependencies',
      'pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-harvest/pip-requirements.txt')

b.run('Quick tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-dgu/ckanext/dgu/tests/ --ckan --with-pylons=%(src_dir)s/ckanext-dgu/test.ini')

b.run('Full tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-dgu/ckanext/dgu/tests/ --ckan --with-pylons=%(src_dir)s/ckanext-dgu/test-core.ini')

