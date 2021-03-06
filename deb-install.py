#!/usr/bin/env python
import sys

from builder_deb import builder as b
b.env['revision'] = 'default'
b.env['instance'] = 'dgu'

b.run('Stop any previously running vm.',
      '%(vm_dir)s/stop-kvm.sh')

b.run('Copy vm',
      'rsync %(base_vm_filepath)s %(vm_dir)s/test.vm')

b.run('Start vm',
      '%(vm_dir)s/start-kvm.sh %(vm_eth)s %(vm_qtap)s 512M %(vm_processors)s %(vm_dir)s/test.vm')

b.run('Setup vm',
      'fab -f ~/vm-fabfile.py -H %(vm_user)s@%(vm_ip)s -p %(vm_password)s setup_vm:instance=%(instance)s')

#b.run('Copy vm pre-ckan',
#      'rsync %(vm_dir)s/test.vm %(vm_dir)s/test-preckan.vm')

b.run('Install CKAN',
      'fab -f ~/vm-fabfile.py -H %(vm_user)s@%(vm_ip)s -p %(vm_password)s install_ckan:instance=%(instance)s')

#b.run('Stop vm',
#      '%(vm_dir)s/stop-kvm.sh')

