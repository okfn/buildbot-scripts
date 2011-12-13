#!/usr/bin/env python

from builder_ckanext import builder as b

b.run('Remove potential conflicts',
      'rm -rf %(pyenv_dir)s/src/datautildate')

b.run('Install datautildate',
      'pip -E %(pyenv_dir)s install -e hg+https://okfn@bitbucket.org/okfn/datautildate#egg=datautildate')

b.run('Install datautildate test deps manually',
      'pip -E %(pyenv_dir)s install nose xlrd gdata')

b.run('Tests',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/datautildate/datautildate/tests')

