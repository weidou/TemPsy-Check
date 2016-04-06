#!/usr/bin/python
import sys
import os
import re
import traceback
  
'''
  Transform the CSV representation of a trace instance
  into a MonPoly format (i.e., /@timestamp event()/)
'''
class TraceTransformation(object):
  
  def __init__(self, source_name, dest_name, sig_name):
    self.sname = source_name
    self.dname = dest_name
    self.signame = sig_name

  def transform_trace(self):
    self.parse_trace()

  def parse_trace(self):
    self.events = []
    try:
      df = open(self.dname, 'w')
      sigf = open(self.signame, 'w')
      regex_line = re.compile(r'''(?P<event>[^,]+),(?P<timestamp>[0-9]+)''')
      with open(self.sname) as sf:
        sf.readline()
        for line in sf:
          if line:
            trace_element = regex_line.search(line)
            event = trace_element.groupdict().pop('event')
            timestamp = trace_element.groupdict().pop('timestamp')
            df.writelines("\t@%s %s()\n" % (timestamp, event))
            if event not in self.events:
              self.events += [event]
              sigf.writelines("\t%s()\n" % event)
    except Exception, e:
      df.close()
      traceback.print_exc()

if __name__ == '__main__':
  for afile in os.listdir("."):
    if afile.endswith(".csv"):
      file_name, file_extension = os.path.splitext(afile)
      csv_file = "{}.csv".format(file_name)
      log_file = "{}.log".format(file_name)
      sig_file = "{}.sig".format(file_name)
      print csv_file, log_file, sig_file
      transform = TraceTransformation(csv_file, log_file, sig_file)
      transform.transform_trace()
