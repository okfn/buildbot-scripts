#!/usr/bin/env python

#!/usr/bin/env python

from builder_ckan import builder as b

b.run('Full tests using postgres and migration...',
      '. %(pyenv_dir)s/bin/activate; %(pyenv_dir)s/bin/nosetests -v %(src_dir)s/ckan/ckan/tests/ --ckan --ckan-migration --with-pylons=%(src_dir)s/ckan/test-core.ini')

