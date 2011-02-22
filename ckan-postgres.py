#!/usr/bin/env python

from builder import Builder
import os

module_name='ckan'
ckan_instance_name='buildandsmoke'
ve_dir='/home/buildslave/ve/bin'
build_dir='/home/buildslave/okfn/full/build'
pyenv_dir=os.path.join(build_dir, ckan_instance_name, 'pyenv')
src_dir=os.path.join(pyenv_dir, 'src')
ckan_repo='https://bitbucket.org/okfn/ckan/raw'

b = Builder(module_name=module_name,
            ckan_instance_name=ckan_instance_name,
            ve_dir=ve_dir,
            build_dir=build_dir,
            pyenv_dir=pyenv_dir,
            src_dir=src_dir,
            ckan_repo=ckan_repo,
            )

cwd = os.getcwd()
assert cwd == build_dir


b.run('Migration tests...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --ckan-migration --with-pylons=%(src_dir)s/ckan/test-core.ini')

b.run('Full tests using postgres...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini')

