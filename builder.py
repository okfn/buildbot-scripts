import commands
import sys
import os

class Builder(object):
    def __init__(self,
                 **env):
        self.env = env

    def print_title(self, msg):
        print '\n### %s' % (msg % self.env)

    def run(self, msg, cmd, is_verbose=True):
        self.print_title(msg)
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
            return output
