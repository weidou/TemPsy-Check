#!/usr/bin/python
import os, argparse, subprocess
from traceTransformation import TraceTransformation
from settings import destDir

"""
Run this script before run.py
"""

def createDirectory(dir='.'):
  if not os.path.exists(dir):
    os.makedirs(dir)

def transformTrace(dir='.'):
  for traceOriginalFile in os.listdir(dir):
    if traceOriginalFile.endswith('csv'):
      fileName, fileExtension = os.path.splitext(traceOriginalFile)
      traceInstanceFile = "{}/{}.xmi".format(destDir, fileName)
      handler = TraceTransformation(
        os.path.join(dir, traceOriginalFile),
        traceInstanceFile)
      handler.transformTrace()

def transformProperties(dir='.'):
  for oclrOriginalFile in os.listdir(dir):
    if oclrOriginalFile.endswith('oclr'):
      fileName, fileExtension = os.path.splitext(oclrOriginalFile)
      oclrInstanceFile = "{}/{}.xmi".format(destDir, fileName)
      subprocess.call(['java', '-jar', 'oclr.jar',
        os.path.join(dir, oclrOriginalFile),
        oclrInstanceFile])

# program entry
if __name__ == '__main__':
  cmdline = argparse.ArgumentParser(usage='usage: prepare.py -p/--property_dir PROPERTY_DIR -t/--trace_dir TRACE_DIR', description='Make instances of traces and properties.')
  cmdline.add_argument('--property_dir',
             '-p',
             action='store',
             help=r'The directory where property files locate',
             dest='propertyDir',
             required=True
            )
  cmdline.add_argument('--trace_dir',
             '-t',
             action='store',
             help=r'The directory where trace files locate',
             dest='traceDir',
             required=True
            )

  args = cmdline.parse_args()
  #create a directory for instances of traces and properties
  createDirectory(destDir)
  print 'Transforming properties...'
  transformProperties(args.propertyDir)
  print 'Transforming traces...'
  transformTrace(args.traceDir)
  print 'Accomplish!'
