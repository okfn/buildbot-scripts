#!/usr/bin/env python
import os

#from mercurial import ui, hg

from builder import Builder

module_name='ckan'
ckan_instance_name='ckan1' # can't call it 'ckan' as it gives problems 
                           # with importing nose plugin
build_dir='/home/buildslave/ckan/build'
pyenv_dir=os.path.join(build_dir, ckan_instance_name, 'pyenv')
src_dir=os.path.join(pyenv_dir, 'src')
ckan_repo='https://github.com/okfn/ckan'
ckan_repo_files=ckan_repo + '/raw'

class CkanBuilder(Builder):
    def get_release_branches(self):
        # Find the latest release branch
        repo = self.get_remote_ckan_repo()
        release_branches = sorted([branch for branch in repo.branchmap() if branch.startswith('release-')])
        return release_branches

    def get_remote_ckan_repo(self):
        return hg.repository(ui.ui(), '%(ckan_repo)s' % self.env)

    def get_local_ckan_repo(self):
        return hg.repository(ui.ui(), '%(src_dir)s/ckan' % self.env)

    def assert_ckan_branch(self):
        '''Checks the ckan src checkout is the correct branch'''
        expected_branch = self.env['revision']
        self.print_title('Assert code branch is: %s' % expected_branch)
        repo = self.get_local_ckan_repo()
        ctx = repo[None]
        branch = ctx.branch()
        assert branch == expected_branch, '%s != %s' % (branch, expected_branch)
    
builder = CkanBuilder(module_name=module_name,
                      ckan_instance_name=ckan_instance_name,
                      build_dir=build_dir,
                      pyenv_dir=pyenv_dir,
                      src_dir=src_dir,
                      ckan_repo=ckan_repo,
                      ckan_repo_files=ckan_repo_files,
                      )

cwd = os.getcwd()
assert cwd == build_dir, 'Need to run from path %s not %s' % (build_dir, cwd)

