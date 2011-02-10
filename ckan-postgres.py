#!/usr/bin/env python

from builder import Builder

module_name='ckan'
builder_name='ckan-sqlite'
db_name=None,
ve_dir='/home/buildslave/ve/bin/'
build_dir='/home/buildslave/okfn/full/build/'
pyenv_dir=os.path.join(build_dir, builder_name, 'pyenv')
src_dir=os.path.join(pyenv_dir, 'src')
ckan_repo='https://bitbucket.org/okfn/ckan/raw'

b = Builder(module_name=module_name,
            builder_name=builder_name,
            db_name=db_name,
            ve_dir=ve_dir,
            build_dir=build_dir,
            pyenv_dir=pyenv_dir,
            src_dir=src_dir,
            ckan_repo=ckan_repo,
            )

import os
cwd = os.getcwd()
assert cwd == build_dir

b.run('Full tests using postgres...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini')


