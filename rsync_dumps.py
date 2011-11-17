import os
import shutil

dump_dir = '/home/buildslave/dumps/'
remote_dir = 'okfn@dgu-live.okfn.org:/var/backup/ckan/dgu/'
gz_dir = '/home/buildslave/dumps_gz/'

cmd = 'rsync --stats -aHxvz --progress --numeric-ids %s %s'%(remote_dir, dump_dir)
print cmd
os.system(cmd)
# Start with the most recent
dumps = os.listdir(dump_dir)
dumps.sort()
dumps.reverse()
for dump in dumps:
    dump_gz = os.path.join(gz_dir, dump + '.gz')
    if not os.path.exists(os.path.join(gz_dir, dump + '.gz')):
        print "Copying and zipping ", dump
        shutil.copyfile(
            os.path.join(dump_dir, dump),
            os.path.join(gz_dir, dump),
        )
        os.system('gzip %s'%os.path.join(gz_dir, dump))

