#!/usr/bin/python
import sys, os, re, traceback
import csv

'''
Transform a trace instance in CSV format into internal XMI format.
'''
class TraceTransformation(object):

  # events register
  events = []

  # templates of the rows of trace elemnts and events
  traceRowTemplate = '  <traceElements index="{}" event="//@events.{}">\n    <timestamp value="{}"/>\n  </traceElements>\n'
  eventRowTemplate = '  <events id="{}" name="{}"/>\n'

  def __init__(self, scrName, destName):
    self.scrName = scrName
    self.destName = destName

  def transformTrace(self):
    self.writeTrace()
    self.writeEvents()

  def writeEvents(self):
    df = open(self.destName, 'a+')
    i = 1
    try:
      for e in self.events:
        df.writelines(self.eventRowTemplate.format(i, e))
        i = i+1
    except Exception, e:
      traceback.print_exc()
    finally:
      df.writelines('</trace:Trace>')
      df.close()

  def writeTrace(self):
    df = open(self.destName, 'wt')
    sf = open(self.scrName, 'rt')
    try:
      df.writelines("<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<trace:Trace xmi:version=\"2.0\" xmlns:xmi=\"http://www.omg.org/XMI\" xmlns:trace=\"http://www.svv.lu/offline/trace/Trace\">\n")
      reader = csv.DictReader(sf, skipinitialspace=True)
      i = 1
      for row in reader:
        e = row['event']
        ts = row['timestamp']
        if e in self.events:
          df.writelines(self.traceRowTemplate.format(i, self.events.index(e), ts))
        else:
          self.events.append(e)
          df.writelines(self.traceRowTemplate.format(i, self.events.index(e), ts))
        i = i+1
    except Exception, e:
      traceback.print_exc()
    finally:
      df.close()
      sf.close()
