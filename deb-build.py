#!/usr/bin/env python
import sys
import os

from builder_deb import builder as b
b.env['revision'] = 'default'

assert b.env['build_dir'].startswith('/home/buildslave/deb/build') # double check
b.run('Emptying build folder',
      'rm -rf %(build_dir)s/*')

b.run('python-ckan - create',
       'virtualenv python-ckan')

b.run('python-ckan - get source',
      'python-ckan/bin/pip -E python-ckan install -e hg+http://bitbucket.org/okfn/ckan@%(revision)s#egg=ckan')
      #'hg clone http://bitbucket.org/okfn/ckan#%(revision)s')

# Extract dependencies
sys.path.append('python-ckan/src/ckan')
import ckan
b.env['ckan_version'] = ckan.__version__
b.env['ckan_build_number'] = b.get_build_number('python-ckan/src/ckan')

present = b.run('Assemble list of present packages',
             r"sed '/\s*#/d;s/==.*//g' python-ckan/src/ckan/requires/lucid_present.txt | sed ':a;N;$!ba; s/\n/ /g'",
             is_verbose=False)
assert present
missing = b.run('Assemble list of missing packages',
             r"sed -n 's/.*#egg=\(.*\)/\1/p;' python-ckan/src/ckan/requires/lucid_missing.txt | sed ':a;N;$!ba; s/\n/ /g'",
             is_verbose=False)
assert missing
other_deps = 'python-ckan-deps '
ckan_deps = ' '.join((present, missing, other_deps))

b.run('python-ckan - create deb package',
      'cd python-ckan; ~/pyenv-tools/bin/python -m buildkit.deb . ckan %(ckan_version)s~%(ckan_build_number)s+lucid http://ckan.org ' + ckan_deps)

b.run('Missing - create',
      'virtualenv missing')

b.run('Missing - get lib dependencies',
      'python-ckan/bin/pip -E missing install --ignore-installed -r python-ckan/src/ckan/requires/lucid_missing.txt')

b.run('Missing - create deb packages',
      'cd missing; ~/pyenv-tools/bin/python -m buildkit.update_all .')

b.run('Conflict - create',
      'mkdir -p conflict/src')

b.run('Conflict - get dependency source',
      'hg clone https://bitbucket.org/okfn/ckan-deps conflict/src/')

b.run('Conflict - rename ckan_deps to ckan-deps',
      'mv conflict/src/ckan_deps conflict/src/ckan-deps')

deps_dir = 'conflict/src'
b.env['ckan_deps_build_number'] = b.get_build_number(deps_dir)

b.run('Conflict - create python-ckan-deps package',
      'cd conflict; ~/pyenv-tools/bin/python -m buildkit.deb . ckan-deps 0.1~%(ckan_deps_build_number)s+lucid http://ckan.org')

b.run('python-ckanext-dgu - create',
      'virtualenv python-ckanext-dgu')

b.run('python-ckanext-dgu - get source',
      'python-ckanext-dgu/bin/pip -E python-ckanext-dgu install --ignore-installed -e hg+https://bitbucket.org/okfn/ckanext-dgu#egg=ckanext-dgu')

b.run('python-ckanext-dgu - get lib dependencies',
      'python-ckanext-dgu/bin/pip -E python-ckanext-dgu install --ignore-installed -r python-ckanext-dgu/src/ckanext-dgu/pip-requirements.txt')

b.run('python-ckanext-dgu - create deb packages',
      'cd python-ckanext-dgu; ~/pyenv-tools/bin/python -m buildkit.update_all .')

sys.path.append('python-ckanext-dgu/src/ckanext-dgu')
import ckanext.dgu
b.env['ckanext_dgu_version'] = ckanext.dgu.__version__

b.run('ckan - get ckan-debs-public repo',
      'hg clone https://bitbucket.org/okfn/ckan-debs-public')

b.run('ckan - put version number in the control file',
      r"sed -e 's/Version: .*/Version: %(ckan_version)s/g' -i ckan-debs-public/ckan/DEBIAN/control")

b.run('ckan - create deb package',
      'cd ckan-debs-public/ckan; dpkg-deb -b . ..')

b.run('ckan-dgu - put version number in the control file',
      r"sed -e 's/Version: .*/Version: %(ckanext_dgu_version)s/g' -i ckan-debs-public/ckan-dgu/DEBIAN/control")

b.run('ckan-dgu - create deb package',
      'cd ckan-debs-public/ckan-dgu; dpkg-deb -b . ..')

