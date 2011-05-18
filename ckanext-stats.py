#!/usr/bin/env python

from builder_ckanext import builder as b
b.env['revision'] = 'default'
b.env['extension_name'] = 'stats'

b.run('Install ckanext-%(extension_name)s',
      'pip -E %(pyenv_dir)s install -e hg+http://bitbucket.org/okfn/ckanext-%(extension_name)s#egg=ckanext-%(extension_name)s')

#b.run('Install dependencies',
#      'pip -E %(pyenv_dir)s install -r %(pyenv_dir)s/src/ckanext-%(extension_name)s/pip-requirements.txt')

b.run('Quick tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-%(extension_name)s/ckanext/%(extension_name)s/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test.ini')

b.run('Full tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanext-%(extension_name)s/ckanext/%(extension_name)s/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini')

