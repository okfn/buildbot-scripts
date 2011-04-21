#!/usr/bin/env python

from builder_ckanext import builder as b

b.run('Remove release version of ckanclient',
      'rm -rf %(pyenv_dir)s/src/ckanclient')

b.run('Install latest ckanclient',
      'pip -E %(pyenv_dir)s install -e hg+http://bitbucket.org/okfn/ckanclient#egg=ckanclient')

b.run('Quick tests...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanclient/ckanclient/tests/ --ckan --with-pylons=%(src_dir)s/ckanclient/test.ini')

b.run('Full tests...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckanclient/ckanclient/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini')

