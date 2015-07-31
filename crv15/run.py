#!/usr/bin/python
import os, sys, argparse, subprocess
from settings import destDir

"""
Main script which runs the monitor.
"""

def invokeJar(*args):
    process = subprocess.Popen(['java', '-jar']+list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr != '':
      return stderr
    else:
      return stdout

def getInstancePath(originalFile):
  fileName, fileExtension = os.path.splitext(os.path.basename(originalFile))
  return os.path.join(destDir, fileName+'.xmi')

# program entry
if __name__ == '__main__':
  cmdline = argparse.ArgumentParser(usage='usage: run.py -p/--properties PROPERTY_FILE_NAME -t/--trace TRACE_FILE_NAME', description='Check an OCLR property over the given trace.')
  cmdline.add_argument('--properties',
             '-p',
             action='store',
             help=r'The property file name',
             dest='property',
             required=True
            )
  cmdline.add_argument('--trace',
             '-t',
             action='store',
             help=r'The trace file name',
             dest='trace',
             required=True
            )

  args = cmdline.parse_args()
  jarArgs = ['oclr-check.jar',
    getInstancePath(args.property),
    getInstancePath(args.trace)]
  sys.stdout.write(invokeJar(*jarArgs))
