#!/usr/bin/env python

import sys; sys.path.append('../../pyenv-tools/lib/python2.6/site-packages/')
from buildkit.repo import BuildCmd
from builder_deb import builder as b
build_dir = b.env['build_dir']

b = BuildCmd()
b.logging({})#{'verbose': True})
#b.clean([], {'build_dir': build_dir})
b.build('latest-common-repo', [], {'build_dir': build_dir})
b.build('latest-instance-repos', [], {'build_dir': build_dir})
b.build('package-if-necessary', [], {'build_dir': build_dir})

