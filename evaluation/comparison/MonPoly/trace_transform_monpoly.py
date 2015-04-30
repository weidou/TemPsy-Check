#!/usr/bin/python
import sys
import os
import re
import traceback
  
'''
  Transform the XMI representation of a trace instance
  into a common format (i.e., /@timestamp event()/)
'''
class TraceTransformation(object):
  
  # the ids of the synthesized traces
  trace_ids = range(1,39)
  
  # the length of the tail
  tail_length = 8
  
  # buffer size
  buffer_size = 8192

  def __init__(self, source_name, dest_name, sig_name):
    self.sname = source_name
    self.dname = dest_name
    self.signame = sig_name

  def transform_trace(self):
    self.parse_events()
    self.parse_trace()

  def parse_events(self):
    lines = self.tail_file()
    sigf = open(self.signame, 'w')
    self.events = {}
    regex = re.compile(r'''id="(?P<id>[0-9]+)"\sname="(?P<name>[a-zA-Z]+)"''')
    for line in lines:
      r = regex.search(line)
      if r:
        event_id = int(r.groupdict().pop('id'))-1
        event_name = r.groupdict().pop('name')
        self.events[event_id] = event_name
        sigf.writelines("\t%s()\n" % event_name)

  def tail_file(self):
    bufsize = self.buffer_size
    fsize = os.stat(self.sname).st_size
    iter = 0
    with open(self.sname) as f: #sys.argv[2]
      if bufsize > fsize:
        bufsize = fsize-1
      data = []
      while True:
        iter +=1
        f.seek(fsize-bufsize*iter)
        data.extend(f.readlines())
        if len(data) >= self.tail_length or f.tell() == 0:
          #print(''.join(data[-length:]))
          return data[-self.tail_length:]
          break
    f.close()

  def parse_trace(self):
    try:
      df = open(self.dname, 'w')
      regex_event = re.compile(r'''event="//@event\.(?P<event>[0-9]+)''') #index="(?P<index>[1-9]+)"\s
      regex_ts = re.compile(r'''value="(?P<value>[0-9]+)"''')
      with open(self.sname) as sf:
        sf.seek(158)
        event = None
        ts = None
        for line in sf:
          if not event:
            event = regex_event.search(line)
          if not ts:
            ts = regex_ts.search(line)
          if event and ts:
            # event_id = r.groupdict().pop('index')
            event_name = self.events[int(event.groupdict().pop('event'))]
            event_time = ts.groupdict().pop('value')
            df.writelines("\t@%s %s()\n" % (event_time, event_name))
            event = None
            ts = None
    except Exception, e:
      df.close()
      traceback.print_exc()

if __name__ == '__main__':
  for filename in os.listdir("."):
    if filename.endswith(".xmi"):
      fileName, fileExtension = os.path.splitext(filename)
      log_name = "{}.log".format(fileName)
      sig_name = "{}.sig".format(fileName)
      transform = TraceTransformation(filename, log_name, sig_name)
      transform.transform_trace()
