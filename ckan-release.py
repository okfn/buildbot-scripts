#!/usr/bin/env python

from builder import Builder

module_name = 'ckan'
branch = 'ckan-1.3'
builder_name = 'ckan-sqlite'
db_name = None,
ve_dir = '/home/buildslave/ve/bin/'
build_dir = '/home/buildslave/okfn/full/build/'
pyenv_dir = os.path.join(build_dir, builder_name, 'pyenv')
src_dir = os.path.join(pyenv_dir, 'src')
ckan_repo = 'https://bitbucket.org/okfn/ckan/raw'

b = Builder(module_name=module_name,
            branch=branch,
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

b.run('Emptying database...', 
      '/home/buildslave/drop-all-tables.sh %(db_name)s buildslave localhost')

assert build_dir.startswith('/home/buildslave/okfn/full/build') # double check
b.run('Emptying build folder...',
      'rm -rf %(build_dir)s/*')

b.run('Getting fabfile from...',
      'wget -O fabfile.py %(ckan_repo)s/default/fabfile.py')

b.run('Running fabfile...',
      '. %(ve_dir)s/bin/activate && %(ve_dir)s/bin/fab config_local:%(build_dir)s,%(builder_name)s,db_host=localhost,db_pass=biomaik15,no_sudo=True,skip_setup_db=True deploy')

b.run('Switching to branch %r...' % branch,
      'hg -R %(src_dir)s/ckan up %(branch)s'

b.run('Copying config for running nosetests...',
      'cp %(build_dir)s%(build_name)s/%(build_name)s.ini %(src_dir)s/ckan/development.ini')

b.run('Quick tests...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test.ini')

b.run('Full tests using postgres...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini')

