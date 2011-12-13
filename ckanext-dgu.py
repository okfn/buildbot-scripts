#!/usr/bin/env python

from builder_ckanext import builder as b

b.run('Remove potential conflicts',
      'rm -rf %(pyenv_dir)s/src/ckanext-* %(pyenv_dir)s/src/ckanclient %(pyenv_dir)s/src/datautildate %(pyenv_dir)s/src/owslib %(pyenv_dir)s/src/apachemiddleware %(pyenv_dir)s/lib/python2.6/site-packages/ckanclient*')

b.run('Install ckanext-dgu',
      'pip -E %(pyenv_dir)s install -e hg+http://bitbucket.org/okfn/ckanext-dgu#egg=ckanext-dgu')

b.run('Install latest ckanext-dgu dependencies',
      'pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-dgu/pip-requirements-latest.txt')

b.run('Install ckanext-harvest dependencies',
      'pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-harvest/pip-requirements.txt')

#b.run('Remove older ckanclient installed by ckanext-harvest pip-requirements.',
#      'rm -rf %(pyenv_dir)s/lib/python2.6/site-packages/ckanclient')

b.run('Quick tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-dgu/ckanext/dgu/tests/ --ckan --with-pylons=%(src_dir)s/ckanext-dgu/test.ini')

b.run('Full tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-dgu/ckanext/dgu/tests/ --ckan --with-pylons=%(src_dir)s/ckanext-dgu/test-core.ini')

