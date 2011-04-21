#!/usr/bin/env python

from builder import Builder
import os

module_name='ckan'
ckan_instance_name='ckan1' # can't call it 'ckan' as it gives problems 
                           # with importing nose plugin
build_dir='/home/buildslave/ckan/build'
pyenv_dir=os.path.join(build_dir, ckan_instance_name, 'pyenv')
src_dir=os.path.join(pyenv_dir, 'src')
ckan_repo='https://bitbucket.org/okfn/ckan/raw'

builder = Builder(module_name=module_name,
                  ckan_instance_name=ckan_instance_name,
                  build_dir=build_dir,
                  pyenv_dir=pyenv_dir,
                  src_dir=src_dir,
                  ckan_repo=ckan_repo,
                  )

cwd = os.getcwd()
assert cwd == build_dir, 'Need to run from path %s not %s' % (build_dir, cwd)


