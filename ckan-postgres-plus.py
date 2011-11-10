#!/usr/bin/env python

#!/usr/bin/env python

from builder_ckan import builder as b

b.run('Migration tests...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --ckan-migration --with-pylons=%(src_dir)s/ckan/test-core.ini')

b.run('Full tests using postgres...',
# removed coverage because it is currently broken
#      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini --with-coverage --cover-package=ckan.')
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --with-pylons=%(src_dir)s/ckan/test-core.ini')

