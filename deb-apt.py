#!/usr/bin/env python
import sys
import os

from builder_deb import builder as b
b.env['revision'] = 'default'

includedeb = 'cd /var/packages/ubuntu_ckan-test; reprepro includedeb lucid %(build_dir)s/'

b.run('Deleting existing packages in apt',
      r'cd /var/packages/ubuntu_ckan-test; reprepro list lucid|sed "s/lucid.*: \(.*\) .*/\1/g" |xargs --no-run-if-empty reprepro remove lucid')

for root, dirs, files in os.walk(b.env['build_dir']):
    for file in files:
        if file.endswith('.deb'):
            deb_filepath = os.path.join(root, file)
            rel_filepath = deb_filepath.replace(b.env['build_dir'], '')
            b.run('%s - include in apt' % rel_filepath,
                  'cd /var/packages/ubuntu_ckan-test; reprepro includedeb lucid %s' % deb_filepath)


