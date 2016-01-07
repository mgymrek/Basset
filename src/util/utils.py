import os
import sys
from subprocess import Popen, PIPE, STDOUT

def message(msg, msgtype='progress'):
    """Send a message to console.
    Args:
        msgtype (str): one of 'progress', 'warning', 'error', or 'debug'
    """
    message = "[%(level)s]: %(text)s" % dict(level=msgtype.upper(), text=msg)
    sys.stderr.write(message.strip() + "\n")

    if msgtype == 'error':
        sys.exit(1)

def RunCommand(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, \
                  stderr=STDOUT, close_fds=True)
    ex = p.wait()
    if ex != 0:
        stdout, stderr = "", ""
        if p.stdout is not None: stdout = p.stdout.read()
        if p.stderr is not None: stderr = p.stderr.read()
        message("ERROR: command '%s' failed.\n\nSTDOUT:%s\nSTDERR:%s"%(cmd, stdout, stderr))
    return ex

def CheckProgram(program):
    """ Check whether a program is installed """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        exe_file = os.path.join(path, program)
        if is_exe(exe_file): return True
    return False
