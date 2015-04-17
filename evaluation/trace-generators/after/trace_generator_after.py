#!/usr/bin/python
from abc import abstractmethod
from random import randrange, sample
from bisect import insort
from math import ceil, floor
import sys, os, argparse, traceback

"""
A synthesized event trace generator
@author: Wei Dou
@date: 27 July 2014
@input: an OCLR property (a scope & a pattern) and a target length
@output: an event trace with random locations of events
"""

# scopes:
## globally
## before [m] 'event' ['comparing_operator' n tu]
## after [m] 'event' ['comparing_operator' n tu]
## between [m1] 'event1' [at least n1 tu] and [m2] 'event2' [at least n2 tu]
## after [m1] 'event1' [at least n1 tu] until [m2] 'event2' [at least n2 tu]

# patterns:
## always 'event'
## eventually ['comparing_operator' n] 'event'
## never [exactly n] 'event'
## 'event1' preceding ['comparing_operator' n tu] 'event2'
## 'event2' responding ['comparing_operator' n tu] 'event1'
## 'event1', # 'comparing_operator' n1 tu 'event2' preceding 'comparing_operator' n2 tu 'event3', # 'comparing_operator' n3 tu 'event4'
## 'event3', # 'comparing_operator' n3 tu 'event4' responding 'comparing_operator' n2 tu 'event1', # 'comparing_operator' n1 tu 'event2'

class PropertyFactory(object):

  @staticmethod
  def create_scope(scope):
    scope_items = scope.split()
    scope_type = scope_items[0]
    if ScopeKeywords.before == scope_type:
      return PropertyFactory.create_uniscope(ScopeKeywords.before, scope)
    elif ScopeKeywords.after == scope_type:
      if ScopeKeywords.after_until not in scope_items:
        return PropertyFactory.create_uniscope(ScopeKeywords.after, scope)
      else:
        return PropertyFactory.create_biscope(ScopeKeywords.after_until, scope)
    elif ScopeKeywords.between_and in scope_items:
      return PropertyFactory.create_biscope(ScopeKeywords.between_and, scope)
    else:
      return Globally()

  @staticmethod
  def create_pattern(pattern):
    pattern_items = pattern.split()
    pattern_type = pattern_items[0]
    if PatternKeywords.universality == pattern_type:
      return PropertyFactory.create_universality(pattern)
    elif PatternKeywords.existence == pattern_type:
      return PropertyFactory.create_occurrences(PatternKeywords.existence,pattern)
    elif PatternKeywords.absence == pattern_type:
      return PropertyFactory.create_occurrences(PatternKeywords.absence,pattern)
    elif PatternKeywords.response in pattern_items:
      effect_cause = pattern.split(PatternKeywords.response)
      effects = effect_cause[0]
      causes = effect_cause[1]
      return PropertyFactory.create_sequence(PatternKeywords.response, causes, effects)
    elif PatternKeywords.precedence in pattern_items:
      cause_effect = pattern.split(PatternKeywords.precedence)
      causes = cause_effect[0]
      effects = cause_effect[1]
      return PropertyFactory.create_sequence(PatternKeywords.precedence, causes, effects)
    else:
      print 'wrong pattern!!'
      traceback.print_exc()

# create scope instances

## before [m] 'event' ['comparing_operator' n tu]
## after [m] 'event' ['comparing_operator' n tu]
  @staticmethod
  def create_uniscope(st, scope):
    scope_items = scope.split()
    scope_items.pop(0)
    ordinal = 1
    if PropertyFactory.is_integer(scope_items[0]):
      ordinal = int(scope_items.pop(0))
    event = scope_items.pop(0).lower()
    RandomTraceGenerator.register_event(event)
    if scope_items:
      scope_items.pop()
      value = int(scope_items.pop())
      comop = scope_items.pop()
      distance = Distance(comop, value)
      return UniScope(st, ordinal, event, distance)
    else:
      return UniScope(st, ordinal, event)

## between [m1] 'event1' [at least n1 tu] and [m2] 'event2' [at least n2 tu]
## after [m1] 'event1' [at least n1 tu] until [m2] 'event2' [at least n2 tu]
  @staticmethod
  def create_biscope(st, scope):
    scope_items = scope.split(st)
    bound1_list = scope_items[0].split()
    bound1_list.pop(0)
    bound2_list = scope_items[1].split()
    ordinal1 = -1
    ordinal2 = -1
    if PropertyFactory.is_integer(bound1_list[0]):
      ordinal1 = int(bound1_list.pop(0))
      ordinal2 = 1
    if PropertyFactory.is_integer(bound2_list[0]):
      ordinal2 = int(bound2_list.pop(0))
      if ordinal1 == -1:
        ordinal1 = 1
    event1 = bound1_list.pop(0).lower()
    event2 = bound2_list.pop(0).lower()
    RandomTraceGenerator.register_event(event1)
    RandomTraceGenerator.register_event(event2)
    distance1 = None
    distance2 = None
    if bound1_list:
      bound1_list.pop()
      value1 = int(bound1_list.pop())
      comop1 = bound1_list.pop()
      distance1 = Distance(comop1, value1)
    if bound2_list:
      bound2_list.pop()
      value2 = int(bound2_list.pop())
      comop2 = bound2_list.pop()
      distance2 = Distance(comop2, value2)
    return BiScope(st, ordinal1, event1, distance1, ordinal2, event2, distance2)

# create pattern instances

## always 'event'
  @staticmethod
  def create_universality(pattern):
    event = pattern.split().pop().lower()
    RandomTraceGenerator.register_event(event)
    return Universality(event)

## eventually ['comparing_operator' n] 'event'
## never [exactly n] 'event'
  @staticmethod
  def create_occurrences(pt, pattern):
    pattern_items = pattern.split()
    event = pattern_items.pop().lower()
    RandomTraceGenerator.register_event(event)
    s = pattern_items.pop()
    if PropertyFactory.is_integer(s):
      times = int(s)
      comop = pattern_items.pop()
      if pt==PatternKeywords.existence:
        return Existence(event, comop, times)
      else:
        return Absence(event, comop, times)
    else:
      if pt==PatternKeywords.existence:
        return Existence(event)
      else:
        return Absence(event)

## 'event1' preceding ['comparing_operator' n tu] 'event2'
## 'event2' responding ['comparing_operator' n tu] 'event1'
## or
## 'event1'[, [# 'comparing_operator' n1 tu] 'event2'] preceding ['comparing_operator' n2 tu] 'event3'[, [# 'comparing_operator' n3 tu] 'event4']
## 'event3'[, [# 'comparing_operator' n3 tu] 'event4'] responding ['comparing_operator' n2 tu] 'event1'[, [# 'comparing_operator' n1 tu] 'event2']
## or
## $eventchain1$ preceding $eventchain2$
## $eventchain2$ responding $eventchain1$
  @staticmethod
  def create_sequence(pt, causes, effects):
    effect_list = effects.split(',')
    cause_list = causes.split(',')
    events = []
    distances = []
    for cause in cause_list:
      raw_event = cause.split()
      event = raw_event.pop().lower()
      RandomTraceGenerator.register_event(event)
      events.append(event)
      if raw_event:
        # pop tu
        raw_event.pop()
        # pop the value
        value = int(raw_event.pop())
        # pop 'least|most|exactly'
        comop = raw_event.pop()
        distances.append(Distance(comop, value))
      else:
        distances.append(None)
    if pt == PatternKeywords.response:
      distances.append(distances.pop(0))
    else:
      distances.pop(0)
    for effect in effect_list:
      raw_event = effect.split()
      event = raw_event.pop().lower()
      RandomTraceGenerator.register_event(event)
      events.append(event)
      if raw_event:
        # pop tu
        raw_event.pop()
        # pop the value
        value = int(raw_event.pop())
        # pop 'least|most|exactly'
        comop = raw_event.pop()
        distances.append(Distance(comop, value))
      else:
        distances.append(None)
    if pt == PatternKeywords.response:
      distances.pop()
    return Sequence(pt, events, distances)

# test whether string s is an integer
  @staticmethod
  def is_integer(s):
    try:
      int(s)
      return True
    except ValueError:
      return False

# trace generator
class RandomTraceGenerator(object):
  # mask event
  mask = 'c'
  # the density of randomness
  density = 0.1
  # fixed proportion of the uniscope boundary
  fixed_proportion = 0.1
  # start point for another trace with scope globally
  i_globally = 0
  # candidate events [a..z]
  candidate_events = list(map(chr, range(97, 123)))
  # the events register for each OCLR property
  events_register = [mask]

  @staticmethod
  def register_event(event):
    if event != RandomTraceGenerator.mask:
      insort(RandomTraceGenerator.events_register, event)
    else:
      RandomTraceGenerator.mask = (set(RandomTraceGenerator.candidate_events)-set(RandomTraceGenerator.events_register)).pop()
      insort(RandomTraceGenerator.events_register, RandomTraceGenerator.mask)

  def __init__(self, property_id, length, scope, pattern):
    self.property_id = property_id
    self.length = length
    self.scope = scope
    self.pattern = pattern

  def open_file(self):
    # trace output file
    self.outputFile = os.path.join(os.getcwd(), '%s_%d_%d_after.xmi' % (self.property_id, self.length, int(10*RandomTraceGenerator.fixed_proportion)))
    # trace output file
    self.outputFile_globally = os.path.join(os.getcwd(), '%s_%d_%d_globally.xmi' % (self.property_id, self.length, int(10*RandomTraceGenerator.fixed_proportion)))
    # trace events locations recording file
    self.locationsFile = os.path.join(os.getcwd(), '%s_%d_%d.locations' % (self.property_id,self.length, int(10*RandomTraceGenerator.fixed_proportion)))
    try:
      # open two output files
      self.f = open(self.outputFile, 'w')
      self.f_globally = open(self.outputFile_globally, 'w')
      self.bf = open(self.locationsFile, 'w')
      print 'writing into file: "%s"\n...' % self.outputFile
    except Exception as e:
      traceback.print_exc()

  def generate_trace(self):
    try:
      # open files
      self.open_file()
      # write trace file header
      self.f.writelines("<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<trace:Trace xmi:version=\"2.0\" xmlns:xmi=\"http://www.omg.org/XMI\" xmlns:trace=\"http://www.svv.lu/offline/trace/Trace\">\n")
      # write globally trace file header
      self.f_globally.writelines("<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<trace:Trace xmi:version=\"2.0\" xmlns:xmi=\"http://www.omg.org/XMI\" xmlns:trace=\"http://www.svv.lu/offline/trace/Trace\">\n")
      # write trace locations file header
      self.bf.writelines("length: %d\n" % self.length)
      # generate an event trace accorrding to the temporal property containing a scope and a pattern
      if self.scope is not None and self.pattern is not None:
        if type(self.scope) == Globally:
          if self.pattern.get_min_length() > self.length:
            print 'The given length is too short!!'
            return
          self.write_globally()
        else:
          scope_min_length = self.scope.get_min_length()
          pattern_min_length = self.pattern.get_min_length()
          if scope_min_length + pattern_min_length > self.length:
            print 'The given length is too short!!'
            return
          if self.scope.scope_type == ScopeKeywords.before:
            self.write_before()
          elif self.scope.scope_type == ScopeKeywords.after:
            self.write_after()
          elif self.scope.scope_type == ScopeKeywords.between_and:
            self.write_betweenand()
          else:
            self.write_afteruntil()
      else:
        print "Please provide a correct pair of scope and pattern!!"
      for e in RandomTraceGenerator.events_register:
        self.f.writelines("  <event id=\"%d\" name=\"%s\"/>\n" % (RandomTraceGenerator.events_register.index(e)+1, e))
        self.f_globally.writelines("  <event id=\"%d\" name=\"%s\"/>\n" % (RandomTraceGenerator.events_register.index(e)+1, e))
      self.f.writelines("</trace:Trace>\n")
      self.f_globally.writelines("</trace:Trace>\n")
      self.f.close()
      self.f_globally.close()
      self.bf.close()
      print 'Done!'
    except Exception as e:
      print 'Unable to write into file %s' % self.outputFile
      #print e
      traceback.print_exc()
      self.f.close()
      self.bf.close()
      os.remove(self.outputFile)
      os.remove(self.locationsFile)
      sys.exit(1)

# core of our trace generator

## depending on different scopes, different strategies are applied
  def write_globally(self):
    try:
      pattern_start = 1
      pattern_end = self.length
      self.write_pattern(pattern_start, pattern_end)
    except Exception:
      traceback.print_exc()

  def write_before(self):
    try:
      pattern_length_bound = self.pattern.get_length_bound()
      # scope start point
      scope_start = int(self.length*RandomTraceGenerator.fixed_proportion) - self.scope.amount+1
      if self.scope.distance:
        scope_end = max(scope_start + self.scope.amount - 1, pattern_length_bound+self.scope.distance.get_lower_bound()+self.scope.amount)
      else:
        scope_end = max(scope_start + self.scope.amount - 1, pattern_length_bound+self.scope.amount)
      # scope end point
      # generate locations for scope event
      self.scope.generate_locations(scope_start, scope_end)
      if self.scope.distance:
        pattern_start = {
          ComparingOperator.at_least : 1,
          ComparingOperator.at_most: self.scope.locations[-1]-self.scope.distance.get_distance(),
          ComparingOperator.exactly: self.scope.locations[-1]-self.scope.distance.get_distance()
        }[self.scope.distance.comparing_operator]
        pattern_end = {
          ComparingOperator.at_least : self.scope.locations[-1]-self.scope.distance.get_distance(),
          ComparingOperator.at_most: self.scope.locations[0]-1,
          ComparingOperator.exactly: self.scope.locations[-1]-self.scope.distance.get_distance()
        }[self.scope.distance.comparing_operator]
      else:
        pattern_start = 1
        pattern_end = self.scope.locations[0]-1
      if 1 < pattern_start:
        self.write_universality(1, pattern_start-1, RandomTraceGenerator.mask)
      RandomTraceGenerator.i_globally = 1
      self.write_pattern(pattern_start, pattern_end)
      RandomTraceGenerator.i_globally = 0
      self.write_occurrences(pattern_end+1, self.length, self.scope.locations, self.scope.event)
    except Exception:
      traceback.print_exc()

  def write_after(self):
    try:
      pattern_length_bound = self.pattern.get_length_bound()
      # scope start point
      scope_start = 1
      scope_end = int(self.length*RandomTraceGenerator.fixed_proportion)
      if scope_end == 0:
        scope_end = self.scope.amount
      if self.scope.distance:
        scope_end = min(scope_end, self.length-pattern_length_bound-self.scope.distance.get_lower_bound())
      else:
        scope_end = min(scope_end, self.length-pattern_length_bound)
      # generate locations for scope event
      self.scope.generate_locations(scope_start, scope_end)
      if self.scope.distance:
        pattern_start = {
          ComparingOperator.at_least : self.scope.locations[-1]+self.scope.distance.get_distance(),
          ComparingOperator.at_most: self.scope.locations[-1]+1,
          ComparingOperator.exactly: self.scope.locations[-1]+self.scope.distance.get_distance()
        }[self.scope.distance.comparing_operator]
        pattern_end = {
          ComparingOperator.at_least : self.length,
          ComparingOperator.at_most: self.scope.locations[-1]+self.scope.distance.get_distance(),
          ComparingOperator.exactly: self.scope.locations[-1]+self.scope.distance.get_distance()
        }[self.scope.distance.comparing_operator]
      else:
        pattern_start = self.scope.locations[-1]+1
        pattern_end = self.length
      self.write_occurrences(scope_start, pattern_start-1, self.scope.locations, self.scope.event)
      RandomTraceGenerator.i_globally = 1
      self.write_pattern(pattern_start, pattern_end)
      RandomTraceGenerator.i_globally = 0
      if self.length > pattern_end:
        self.write_universality(pattern_end+1, self.length, RandomTraceGenerator.mask)
    except Exception:
      traceback.print_exc()

  def write_betweenand(self):
    try:
      scope_length_bound = self.scope.get_length_bound()
      pattern_length_bound = self.pattern.get_length_bound()
      length_bound = scope_length_bound + pattern_length_bound
      if self.scope.ordinal1 == -1 and self.scope.ordinal2 == -1:
        if length_bound >= self.length:
          self.write_biscope_segment(1, self.length, self.pattern.get_min_length())
          return
        segments = range(1, self.length, max(length_bound, int((len(RandomTraceGenerator.events_register)-1)/RandomTraceGenerator.density)))
        # add the last segment if possible
        if self.length-segments[-1]+1 >= length_bound:
          segments.append(self.length+1)
        for i in range(0, len(segments)-1):
          scope_start = segments[i]
          scope_end = segments[i+1]-1
          self.write_biscope_segment(scope_start, scope_end, pattern_length_bound)
        if segments[-1] < self.length+1:
          self.write_universality(segments[-1], self.length, RandomTraceGenerator.mask)
      else:
        scope_start = 1
        scope_end = self.length
        self.write_biscope_segment(scope_start, scope_end, pattern_length_bound)
    except Exception:
      traceback.print_exc()

  def write_afteruntil(self):
    try:
      scope_length_bound = self.scope.get_length_bound()
      pattern_length_bound = self.pattern.get_length_bound()
      length_bound = scope_length_bound + pattern_length_bound
      if self.scope.ordinal1 == -1 and self.scope.ordinal2 == -1:
        if length_bound >= self.length:
          self.write_afteruntil_segment(1, self.length, self.pattern.get_min_length())
          return
        segments = range(1, self.length, max(length_bound, int((len(RandomTraceGenerator.events_register)-1)/RandomTraceGenerator.density)))
        # add the last segment
        if self.length-segments[-1]+1 >= length_bound:
          segments.append(self.length+1)
        for i in range(0, len(segments)-2):
          scope_start = segments[i]
          scope_end = segments[i+1]-1
          self.write_biscope_segment(scope_start, scope_end, pattern_length_bound)
        self.write_afteruntil_segment(segments[n-2], segments[n-1]-1, pattern_length_bound)
        if segments[-1] < self.length+1:
          self.write_universality(segments[-1], self.length, RandomTraceGenerator.mask)
      else:
        scope_start = 1
        scope_end = self.length
        self.write_afteruntil_segment(scope_start, scope_end, pattern_length_bound)
    except Exception:
      traceback.print_exc()

  def write_biscope_segment(self, scope_start, scope_end, pattern_length_bound):
    try:
      self.scope.generate_locations(scope_start, scope_end, pattern_length_bound)
      if self.scope.distance1:
        pattern_start = self.scope.locations1[-1]+self.scope.distance1.get_distance()
      else:
        pattern_start = self.scope.locations1[-1]+1
      if self.scope.distance2:
        pattern_end = self.scope.locations2[0]-self.scope.distance2.get_distance()
      else:
        pattern_end = self.scope.locations2[0]-1
      self.write_occurrences(scope_start, pattern_start-1, self.scope.locations1, self.scope.event1)
      if pattern_start <= pattern_end:
        self.write_pattern(pattern_start, pattern_end)
      self.write_occurrences(pattern_end+1, scope_end, self.scope.locations2, self.scope.event2)
    except Exception:
      traceback.print_exc()

  def write_afteruntil_segment(self, scope_start, scope_end, pattern_length_bound):
    try:
      if abs(self.scope.ordinal2) == 1:
        self.scope.generate_locations1(scope_start, scope_end, pattern_length_bound)
        pattern_end = scope_end
      else:
        self.scope.generate_locations(scope_start, scope_end, pattern_length_bound)
        self.scope.locations2.pop() # make the specific bound2 disappeared
        pattern_end = self.scope.locations2[0]-1
      if self.scope.distance1:
        pattern_start = self.scope.locations1[-1]+self.scope.distance1.get_distance()
      else:
        pattern_start = self.scope.locations1[-1]+1
      self.write_occurrences(scope_start, pattern_start-1, self.scope.locations1, self.scope.event1)
      self.write_pattern(pattern_start, pattern_end)
      if abs(self.scope.ordinal2) == 1:
        self.write_universality(pattern_end+1, scope_end, RandomTraceGenerator.mask)
      else:
        self.write_occurrences(pattern_end+1, scope_end, self.scope.locations2, self.scope.event2)
    except Exception:
      traceback.print_exc()

## generating events for patterns

  def write_pattern(self, start, end):
    try:
      if type(self.pattern) == Universality:
        self.write_universality(start, end, self.pattern.event)
      elif type(self.pattern) == Absence:
        self.pattern.generate_locations(start, end)
        if self.pattern.amount == 0:
          self.write_universality(start, end, RandomTraceGenerator.mask)
        else:
          self.write_occurrences(start, end, self.pattern.locations, self.pattern.event)
      elif type(self.pattern) == Existence:
        self.pattern.generate_locations(start, end)
        self.write_occurrences(start, end, self.pattern.locations, self.pattern.event)
      else: #if type(self.pattern) == Sequence:
        if type(self.scope) == BiScope and self.scope.ordinal1 == -1 and self.scope.ordinal2 == -1:
          self.pattern.generate_locations(start, end)
          self.write_sequence_segment(start, end)
        else:
          self.write_sequence(start, end)
    except Exception:
      traceback.print_exc()

  def write_universality(self, start, end, event):
    j = RandomTraceGenerator.events_register.index(event)
    i = start
    try:
      if RandomTraceGenerator.i_globally:
        while i<=end:
          self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, j, int(i*Distance.unit)))
          self.f_globally.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (RandomTraceGenerator.i_globally, j, int(RandomTraceGenerator.i_globally*Distance.unit)))
          i = i+1
          RandomTraceGenerator.i_globally = RandomTraceGenerator.i_globally + 1
        if start <= end:
          self.bf.writelines("%d-%d\t\t\t\t%s\n" % (start, end, event))
      else:
        while i<=end:
          self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, j, int(i*Distance.unit)))
          i = i+1
        if start <= end:
          self.bf.writelines("%d-%d\t\t\t\t%s\n" % (start, end, event))
    except Exception:
      traceback.print_exc()

  def write_occurrences(self, start, end, locations, event):
    try:
      i = start
      mark = i
      mask_index = RandomTraceGenerator.events_register.index(RandomTraceGenerator.mask)
      event_index = RandomTraceGenerator.events_register.index(event)
      location_iter = iter(locations)
      try:
        j = next(location_iter)
      except StopIteration:
        j = end+1
      if RandomTraceGenerator.i_globally:
        while i<=end:
          if i<j:
            self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, mask_index, int(i*Distance.unit)))
            self.f_globally.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (RandomTraceGenerator.i_globally, mask_index, int(RandomTraceGenerator.i_globally*Distance.unit)))
          else:
            self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, event_index, int(i*Distance.unit)))
            self.f_globally.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (RandomTraceGenerator.i_globally, event_index, int(RandomTraceGenerator.i_globally*Distance.unit)))
            if mark<=i-1:
              self.bf.writelines("%d-%d\t\t\t\t%s\n" % (mark, i-1, RandomTraceGenerator.mask))
            self.bf.writelines("%d\t\t\t\t\t%s\n" % (i, event))
            mark = i+1
            try:
              j = next(location_iter)
            except StopIteration:
              j = end+1
          i = i+1
          RandomTraceGenerator.i_globally = RandomTraceGenerator.i_globally + 1
      else:
        while i<=end:
          if i<j:
            self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, mask_index, int(i*Distance.unit)))
          else:
            self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, event_index, int(i*Distance.unit)))
            if mark<=i-1:
              self.bf.writelines("%d-%d\t\t\t\t%s\n" % (mark, i-1, RandomTraceGenerator.mask))
            self.bf.writelines("%d\t\t\t\t\t%s\n" % (i, event))
            mark = i+1
            try:
              j = next(location_iter)
            except StopIteration:
              j = end+1
          i = i+1
      if mark<=end:
        self.bf.writelines("%d-%d\t\t\t\t%s\n" % (mark, end, RandomTraceGenerator.mask))
    except Exception:
      traceback.print_exc()

  def write_sequence(self, start, end):
    try:
      pattern_length_bound = self.pattern.get_length_bound()
      segment_length = max(pattern_length_bound, int(self.pattern.amount/RandomTraceGenerator.density))
      # calculate the segments needed for this sequence pattern
      segments = range(start, end, segment_length)
      # add the last segment
      if end-segments[-1]+1 >= pattern_length_bound:
        segments.append(end+1)
      for i in range(0, len(segments)-1):
        j = segments[i]
        k = segments[i+1]
        self.pattern.generate_locations(j, k-1)
        self.write_sequence_segment(j, k-1)
      if segments[-1] != end+1:
        self.write_universality(segments[-1], end, RandomTraceGenerator.mask)
    except Exception:
      traceback.print_exc()

  def write_sequence_segment(self, start, end):
    try:
      i = start
      mark = i
      mask_index = RandomTraceGenerator.events_register.index(RandomTraceGenerator.mask)
      location_iter = iter(self.pattern.locations)
      try:
        j = next(location_iter)
      except StopIteration:
        j = end+1
      if RandomTraceGenerator.i_globally:
        while i<=end:
          if i<j:
            self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, mask_index, int(i*Distance.unit)))
            self.f_globally.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (RandomTraceGenerator.i_globally, mask_index, int(RandomTraceGenerator.i_globally*Distance.unit)))
          else:
            self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, RandomTraceGenerator.events_register.index(self.pattern.events_dict[i]), int(i*Distance.unit)))
            self.f_globally.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (RandomTraceGenerator.i_globally, RandomTraceGenerator.events_register.index(self.pattern.events_dict[i]), int(RandomTraceGenerator.i_globally*Distance.unit)))
            if mark<=i-1:
              self.bf.writelines("%d-%d\t\t\t\t%s\n" % (mark, i-1, RandomTraceGenerator.mask))
            self.bf.writelines("%d\t\t\t\t\t%s\n" % (i, self.pattern.events_dict[i]))
            mark = i+1
            try:
              j = next(location_iter)
            except StopIteration:
              j = end+1
          i = i+1
          RandomTraceGenerator.i_globally = RandomTraceGenerator.i_globally + 1
      else:
        while i<=end:
          if i<j:
            self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, mask_index, int(i*Distance.unit)))
          else:
            self.f.writelines("  <traceElements index=\"%d\" event=\"//@event.%d\">\n  <timestamp value=\"%d\"/>\n  </traceElements>\n" % (i, RandomTraceGenerator.events_register.index(self.pattern.events_dict[i]), int(i*Distance.unit)))
            if mark<=i-1:
              self.bf.writelines("%d-%d\t\t\t\t%s\n" % (mark, i-1, RandomTraceGenerator.mask))
            self.bf.writelines("%d\t\t\t\t\t%s\n" % (i, self.pattern.events_dict[i]))
            mark = i+1
            try:
              j = next(location_iter)
            except StopIteration:
              j = end+1
          i = i+1
      if mark<=end:
        self.bf.writelines("%d-%d\t\t\t\t%s\n" % (mark, end, RandomTraceGenerator.mask))
    except Exception:
      traceback.print_exc()

# classes of Scopes and Patterns

## enumeration
class ComparingOperator(object):
  at_least = 'least'
  at_most = 'most'
  exactly = 'exactly'

## auxiliary class for identifying scopes
class ScopeKeywords(object):
  globally = 'globally'
  before = 'before'
  after = 'after'
  between_and = 'and'
  after_until = 'until'

# scopes

class Globally(object):
  pass

## before & after
class UniScope(object):

  scope_type = 'UniScope'

  def __init__(self, st, ordinal, event, distance=None):
    self.scope_type = st
    self.amount = ordinal
    self.ordinal = ordinal
    self.event = event
    self.distance = distance

  def get_min_length(self):
    if self.distance:
      if self.scope_type == ScopeKeywords.before:
        return max(self.amount, self.distance.get_lower_bound())
      else:
        return self.amount+self.distance.get_lower_bound()
    else:
      return self.amount

  def generate_locations(self, start, end):
    self.locations = sorted(sample(xrange(start, end), self.amount-1))
    self.locations.append(end)

## between-and & after-until
class BiScope(object):

  scope_type = 'BiScope'

  def __init__(self, st, ordinal1, event1, distance1, ordinal2, event2, distance2):
    self.scope_type = st
    self.amount = abs(ordinal1) + abs(ordinal2)
    self.ordinal1 = ordinal1
    self.event1 = event1
    self.distance1 = distance1
    self.ordinal2 = ordinal2
    self.event2 = event2
    self.distance2 = distance2

  def get_min_length(self):
    if hasattr(self, "min_length"):
      return self.min_length
    self.min_length1 = abs(self.ordinal1)
    self.min_length2 = abs(self.ordinal2)
    if self.distance1:
      self.min_length1 = self.min_length1 + self.distance1.get_lower_bound()
    if self.distance2:
      self.min_length2 = max(self.min_length2, self.distance2.get_lower_bound())
    self.min_length = self.min_length1+self.min_length2
    return self.min_length

  def get_length_bound(self):
    if hasattr(self, "max_length"):
      return self.max_length
    self.max_length1 = abs(self.ordinal1)
    self.max_length2 = abs(self.ordinal2)
    if self.distance1:
      self.max_length1 = self.max_length1 + self.distance1.get_upper_bound()
    if self.distance2:
      self.max_length2 = max(self.max_length2, self.distance2.get_upper_bound())
    self.max_length=self.max_length1+self.max_length2
    return self.max_length

  def generate_locations(self, start, end, pattern_length_bound):
    self.generate_locations1(start, end, pattern_length_bound)
    self.generate_locations2(start, end, pattern_length_bound)

  def generate_locations1(self, start, end, pattern_length_bound):
    if self.distance1:
      upper_bound1 = end - self.distance1.get_lower_bound() - pattern_length_bound - self.min_length2
    else:
      upper_bound1 = end - pattern_length_bound - self.min_length2
    ordinal1 = abs(self.ordinal1)
    if self.ordinal1 != -1 or self.ordinal2 != -1:
      upper_bound1 = max(upper_bound1, start+max(ordinal1, int((end-start)*RandomTraceGenerator.density)))
    self.locations1 = sorted(sample(xrange(start, upper_bound1+1), ordinal1))

  def generate_locations2(self, start, end, pattern_length_bound):
    ordinal2 = abs(self.ordinal2)
    d1 = 0
    if self.distance1:
      d1 = self.distance1.get_lower_bound()-1
    d2 = 1
    if self.distance2:
      d2 = max(1, self.distance2.get_lower_bound()-ordinal2)
    lower_bound2 = self.locations1[-1]+d1+pattern_length_bound+d2
    if self.ordinal1 != -1 or self.ordinal2 != -1:
      lower_bound2 = max(lower_bound2, end+1-max(ordinal2, int((end-start)*RandomTraceGenerator.density)))
    self.locations2 = sorted(sample(xrange(lower_bound2, end+1), abs(self.ordinal2)))

## auxiliary class for identifying patterns
class PatternKeywords(object):

  universality = 'always'
  existence = 'eventually'
  absence = 'never'
  response = 'responding'
  precedence = 'preceding'

# patterns

class Universality(object):

  def __init__(self, event):
    self.event = event
    self.amount = 0

  def get_min_length(self):
    return 1

  def get_length_bound(self):
    return 1

class Existence(object):

  def __init__(self, event, comop=None, times=1):
    self.comparing_operator = comop
    self.times = times
    self.event = event
    self.amount = 0

  def get_min_length(self):
    return self.times

  def get_length_bound(self):
    return self.times

  def get_amount(self, bound):
    return {
      ComparingOperator.at_least : randrange(self.times, bound+1),
      ComparingOperator.at_most  : randrange(0, self.times+1),
      ComparingOperator.exactly  : self.times,
    }.get(self.comparing_operator, 1)

  def generate_locations(self, start, end):
    self.amount = self.get_amount(max(self.times, int((end-start+1)*RandomTraceGenerator.density)))
    self.locations = sorted(sample(xrange(start, end+1), self.amount))

class Absence(object):

  def __init__(self, event, comop=None, times=0):
    self.comparing_operator = comop
    self.times = times
    self.event = event
    self.amount = 0

  def get_min_length(self):
    return 0

  def get_length_bound(self):
    return 1

  def get_amount(self, bound):
    n = randrange(0, bound+1)
    while n != 0 and n == self.times:
      n = randrange(0, bound+1)
    return n

  def generate_locations(self, start, end):
    if self.comparing_operator is None:
      self.amount = 0
    else:
      self.amount = self.get_amount(max(self.times-1, end-start+1))
    # self.locations = []
    if self.amount:
      self.locations = sorted(sample(xrange(start, end+1), self.amount))
    # else:
    #   self.locations = [end]

## precedence & response
class Sequence(object):

  pattern_type = 'Sequence'

  def __init__(self, pt, events, distances=[]):
    self.pattern_type = pt
    self.amount = len(events)
    self.events = events
    self.distances = distances
    # insert None to the head of the distances list
    self.distances.insert(0,None)
    self.prepare_bounds()

  def prepare_bounds(self):
    # prepare to calculate backward distances
    self.distances.append(None)
    self.distances.reverse()
    self.distances.pop()
    n = 0
    self.events_bounds = []
    for d in self.distances:
      if d is None:
        n = n+1
      else:
        n = n + d.get_upper_bound()
      self.events_bounds.append(n)
    # restore distances
    self.distances.append(None)
    self.distances.reverse()
    self.distances.pop()

  def generate_locations(self, start, end):
    upper_bounds = self.cal_upper_bounds(end)
    self.locations = []
    self.events_dict = {}
    i = 0
    temp = start-1
    while i < self.amount:
      upper_bound = upper_bounds[i]
      if self.distances[i]:
        temp = self.distances[i].get_location(temp, upper_bound)
      else:
        temp = randrange(temp+1, upper_bound+1)
      self.locations.append(temp)
      self.events_dict[temp] = self.events[i]
      i = i+1

  def cal_upper_bounds(self, end):
    # initialize the list of upper_bounds
    upper_bounds = []
    for i in self.events_bounds:
      upper_bounds.append(end-i+1)
    upper_bounds.reverse()
    return upper_bounds

  def get_min_length(self):
    n = 0
    for d in self.distances:
      if d is None:
        n = n+1
      else:
        n = n + d.get_lower_bound()
    return n

  def get_length_bound(self):
    n = 0
    for d in self.distances:
      if d is None:
        n = n+2 # give one more space possibility
      else:
        n = n + d.get_upper_bound()
    return n

## class of time distance
class Distance(object):

  unit = 1.0 # one unit equals the distance between two consecutive events

  def __init__(self, comop, value):
    self.comparing_operator = comop
    self.value = value

  def get_distance(self, bound=0):
    least = int(ceil(self.value/Distance.unit))
    most = int(floor(self.value/Distance.unit))
    if bound == 0:
      return least
    else:
      return {
        ComparingOperator.at_least  : randrange(least, max(least, bound)+1),
        ComparingOperator.at_most   : randrange(1, max(most, 1)+1),
        ComparingOperator.exactly   : least
      }[self.comparing_operator]

  def get_upper_bound(self):
    return {
      ComparingOperator.at_least  : int((1+RandomTraceGenerator.density)*ceil(self.value/Distance.unit)),
      ComparingOperator.at_most   : int(self.value/Distance.unit),
      ComparingOperator.exactly   : int(self.value/Distance.unit)
    }[self.comparing_operator]

  def get_lower_bound(self):
    return {
      ComparingOperator.at_least  : int(ceil(self.value/Distance.unit)),
      ComparingOperator.at_most   : 1,
      ComparingOperator.exactly   : int(self.value/Distance.unit)
    }[self.comparing_operator]

  def get_location(self, start, end):
    return start+self.get_distance(end-start)

# program entry
if __name__ == '__main__':
  cmdline = argparse.ArgumentParser(usage='usage: trace_generator_after_variable_boundary.py -s scope -p pattern -l 10000', description='Generate a random trace with a specific length.')
  cmdline.add_argument('--scope',
             '-s',
             action='store',
             help=r'The scope of a temporal property',
             dest='ascope',
             required=True
            )
  cmdline.add_argument('--pattern',
             '-p',
             action='store',
             help=r'The pattern of a temporal property',
             dest='apattern',
             required=True
            )
  cmdline.add_argument('--id',
             '-i',
             action='store',
             help=r'The id of a temporal property',
             dest='id',
             required=True
            )
  cmdline.add_argument('--length',
             '-l',
             action='store',
             help=r'The length of the trace',
             dest='length',
             required=True
            )

  args = cmdline.parse_args()
  length = int(args.length)
  various_proportions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
  # instantiate the scope and pattern
  scope = PropertyFactory.create_scope(args.ascope)
  pattern = PropertyFactory.create_pattern(args.apattern)

  for p in various_proportions:
    RandomTraceGenerator.fixed_proportion = p
    generator = RandomTraceGenerator(args.id, length, scope, pattern)
    generator.generate_trace()
