import commands
import sys
import os

class Builder(object):
    def __init__(self,
                 **env):
        self.env = env

    def run(msg, cmd, is_verbose=True):
        print '\n### %s' % msg
        cmd = cmd % self.env
        print cmd
        if is_verbose:
            if os.system(cmd):
                print "Error: Couldn't run command: %s" % (cmd)
                sys.exit(1)
        else:
            (status, output) = commands.getstatusoutput(cmd)
            if status:
                print output
                print "Error: Couldn't run command: %s" % (cmd)
                sys.exit(1)
