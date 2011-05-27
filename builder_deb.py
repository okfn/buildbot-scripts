#!/usr/bin/env python
import os

from builder import Builder
from mercurial import ui, hg

#module_name='ckan'
build_dir='/home/buildslave/deb/build'
#pyenv_dir=os.path.join(build_dir, ckan_instance_name, 'pyenv')
#src_dir=os.path.join(pyenv_dir, 'src')
#ckan_repo='https://bitbucket.org/okfn/ckan'
#ckan_repo_files=ckan_repo + '/raw'

vm_dir = '~/Vms'
base_vm_filepath = os.path.expandvars('~/Vms/ckan_4/tmpbfoGvb.qcow2')
vm_eth = 'eth0'
vm_qtap = 'qtap0'
vm_processors = 1
vm_ip = '192.168.100.4'
vm_user = 'ubuntu'
vm_password = 'ubuntu'

class DebBuilder(Builder):
    def get_build_number(self, repo_path):
        repo = hg.repository(ui.ui(), repo_path)
        return len(repo.changelog)
   

builder = DebBuilder(
#                      module_name=module_name,
#                      ckan_instance_name=ckan_instance_name,
                      build_dir=build_dir,
#                      pyenv_dir=pyenv_dir,
#                      src_dir=src_dir,
#                      ckan_repo=ckan_repo,
#                      ckan_repo_files=ckan_repo_files,
                       vm_dir=vm_dir,
                       base_vm_filepath=base_vm_filepath,
                       vm_eth=vm_eth,
                       vm_qtap=vm_qtap,
                       vm_processors=vm_processors,
                       vm_ip=vm_ip,
                       vm_user=vm_user,
                       vm_password=vm_password,
                      )

cwd = os.getcwd()
assert cwd == build_dir, 'Need to run from path %s not %s' % (build_dir, cwd)


