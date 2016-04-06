#!/usr/bin/python
from abc import abstractmethod
from random import randrange, sample
from bisect import insort
from math import ceil, floor
import sys, os, argparse, traceback

"""
A synthesized event trace generator
@author: Wei Dou
@date created: 27 July 2014
@date modified: 20 April 2015
@version: 1.3
@input: an TemPsy property (a scope & a pattern) and a target length
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
    cause_size = 0
    for cause in cause_list:
      cause_size = cause_size + 1
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
        distances.append(Distance(comop.strip('#'), value))
      else:
        distances.append(None)
    if pt == PatternKeywords.response:
      distances.append(distances.pop(0))
    else:
      distances.pop(0)
    effectDistances = []
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
        effectDistances.append(Distance(comop.strip('#'), value))
      else:
        effectDistances.append(None)
    if pt == PatternKeywords.response:
      effectDistances.pop(0)
    distances += effectDistances
    return Sequence(pt, events, distances, cause_size)

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
  # head of scope between_and
  between_start = 1
  # tail of scope between_and
  between_end = 1
  # fixed length of each segments
  fixed_length = 2000
  # the number of segments
  segments_number = 1
  # candidate events [a..z]
  candidate_events = list(map(chr, range(97, 123)))
  # the events register for each TemPsy property
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
    self.timestamp = 0

  def open_file(self):
    # trace output file
    self.outputFile = os.path.join(os.getcwd(), '%s_%d_%d_between_mult_fixed_length.csv' % (self.property_id, self.length, RandomTraceGenerator.segments_number/5))
    # trace events locations recording file
    self.locationsFile = os.path.join(os.getcwd(), '%s_%d_%d_between_mult_fixed_length.locations.txt' % (self.property_id,self.length,RandomTraceGenerator.segments_number/5))
    try:
      # open two output files
      self.f = open(self.outputFile, 'w')
      self.bf = open(self.locationsFile, 'w')
      print 'writing into file: "%s"\n...' % self.outputFile
    except Exception as e:
      traceback.print_exc()

  def generate_trace(self):
    try:
      # open files
      self.open_file()
      # write trace file header
      self.f.writelines("event,timestamp\n")
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
      self.f.close()
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
      scope_start = self.length-max(int(self.length*RandomTraceGenerator.density), self.scope.size)+1
      if self.scope.distance:
        scope_start = max(scope_start, pattern_length_bound+self.scope.distance.get_lower_bound())
      else:
        scope_start = max(scope_start, pattern_length_bound+1)
      # scope end point
      scope_end = self.length
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
      self.write_pattern(pattern_start, pattern_end)
      self.write_occurrences(pattern_end+1, self.length, self.scope.locations, self.scope.event)
    except Exception:
      traceback.print_exc()

  def write_after(self):
    try:
      pattern_length_bound = self.pattern.get_length_bound()
      # scope start point
      scope_start = 1
      scope_end = max(int(self.length*RandomTraceGenerator.density), self.scope.size)
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
      self.write_pattern(pattern_start, pattern_end)
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
        segments = sorted(sample(range(1, self.length, RandomTraceGenerator.fixed_length), RandomTraceGenerator.segments_number))
        scope_end = 0
        for i in segments:
          scope_start = i
          if scope_end+1 < scope_start:
            self.write_universality(scope_end+1, scope_start-1, RandomTraceGenerator.mask)
          scope_end = i+RandomTraceGenerator.fixed_length-1
          self.write_biscope_segment(scope_start, scope_end, pattern_length_bound)
        if segments[-1]+RandomTraceGenerator.fixed_length-1 < self.length:
          self.write_universality(segments[-1]+RandomTraceGenerator.fixed_length, self.length, RandomTraceGenerator.mask)
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
        if self.pattern.size == 0:
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
    i = start
    try:
      while i<=end:
        self.timestamp = self.timestamp + int(Distance.unit)
        self.f.writelines("%s,%d\n" % (event, self.timestamp))
        i = i+1
      if start <= end:
        self.bf.writelines("%d-%d\t\t\t\t%s\n" % (start, end, event))
    except Exception:
      traceback.print_exc()

  def write_occurrences(self, start, end, locations, event):
    try:
      i = start
      mark = i
      location_iter = iter(locations)
      try:
        j = next(location_iter)
      except StopIteration:
        j = end+1
      while i<=end:
        self.timestamp = self.timestamp + int(Distance.unit)
        if i<j:
          self.f.writelines("%s,%d\n" % (RandomTraceGenerator.mask, self.timestamp))
        else:
          self.f.writelines("%s,%d\n" % (event, self.timestamp))
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
      segment_length = max(pattern_length_bound, int(self.pattern.size/RandomTraceGenerator.density))
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
      location_iter = iter(self.pattern.locations)
      timestamp_iter = iter(self.pattern.timestamp_distances)
      try:
        j = next(location_iter)
        t = next(timestamp_iter)
      except StopIteration:
        j = end+1
      while i<=end:
        if i<j:
          self.timestamp = self.timestamp + int(Distance.unit)
          self.f.writelines("%s,%d\n" % (RandomTraceGenerator.mask, self.timestamp))
        else:
          self.timestamp = self.timestamp + t
          self.f.writelines("%s,%d\n" % (self.pattern.events_dict[i], self.timestamp))
          if mark<=i-1:
            self.bf.writelines("%d-%d\t\t\t\t%s\n" % (mark, i-1, RandomTraceGenerator.mask))
          self.bf.writelines("%d\t\t\t\t\t%s\n" % (i, self.pattern.events_dict[i]))
          mark = i+1
          try:
            j = next(location_iter)
            t = next(timestamp_iter)
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
    self.size = ordinal
    self.ordinal = ordinal
    self.event = event
    self.distance = distance

  def get_min_length(self):
    if self.distance:
      if self.scope_type == ScopeKeywords.before:
        return max(self.size, self.distance.get_lower_bound())
      else:
        return self.size+self.distance.get_lower_bound()
    else:
      return self.size

  def generate_locations(self, start, end):
    self.locations = sorted(sample(xrange(start, end+1), self.size))

## between-and & after-until
class BiScope(object):

  scope_type = 'BiScope'

  def __init__(self, st, ordinal1, event1, distance1, ordinal2, event2, distance2):
    self.scope_type = st
    self.size = abs(ordinal1) + abs(ordinal2)
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
    self.locations1 = [start]

  def generate_locations2(self, start, end, pattern_length_bound):
    self.locations2 = [end]

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
    self.size = 0

  def get_min_length(self):
    return 1

  def get_length_bound(self):
    return 1

class Existence(object):

  def __init__(self, event, comop=None, times=1):
    self.comparing_operator = comop
    self.times = times
    self.event = event
    self.size = 0

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
    self.size = self.get_amount(max(self.times, int((end-start+1)*RandomTraceGenerator.density)))
    self.locations = sorted(sample(xrange(start, end+1), self.size))

class Absence(object):

  def __init__(self, event, comop=None, times=0):
    self.comparing_operator = comop
    self.times = times
    self.event = event
    self.size = 0

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
      self.size = 0
    else:
      self.size = self.get_amount(max(self.times-1, end-start+1))
    # self.locations = []
    if self.size:
      self.locations = sorted(sample(xrange(start, end+1), self.size))
    # else:
    #   self.locations = [end]

## precedence & response
class Sequence(object):

  pattern_type = 'Sequence'

  def __init__(self, pt, events, distances, cause_size):
    self.pattern_type = pt
    self.size = len(events)
    self.events = events
    self.distances = distances
    self.cause_size = cause_size
    self.effect_size = self.size - self.cause_size
    # make size(distances) = self.size
    self.distances.insert(0,None)

  def generate_locations(self, start, end):
    self.locations = []
    self.timestamp_distances = []
    self.events_dict = {}
    i = 0
    location1 = randrange(start, end-self.size+2)
    location2 = randrange(location1+self.cause_size, end-self.effect_size+2)
    d = self.distances[self.cause_size]
    if d is not None:
      location2 = d.get_location(location1+self.cause_size, end-self.effect_size+1)
    location = location1
    while i < self.size:
      self.locations.append(location)
      self.events_dict[location] = self.events[i]
      d = self.distances[i]
      if d is None:
        self.timestamp_distances.append(randrange(1,6)*int(Distance.unit))
      else:
        if i == self.cause_size:
          self.timestamp_distances.append(max(int(Distance.unit), d.get_real_distance()-location2+previous_location+1))
        else:
          self.timestamp_distances.append(d.get_real_distance())
      i = i+1
      if i == self.cause_size:
        previous_location = location
        location = location2
      else:
        location = location + 1

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
    least = int(ceil(self.value/Distance.unit))
    most = int(floor(self.value/Distance.unit))
    return min(end, start +
              {
                ComparingOperator.at_least  : randrange(least-1, max(least, end-start)),
                ComparingOperator.at_most   : randrange(0, max(most, 1)),
                ComparingOperator.exactly   : randrange(0, max(most, 1)),
              }[self.comparing_operator])

  def get_real_distance(self):
    return {
      ComparingOperator.at_least  : randrange(self.value, int((1+RandomTraceGenerator.density)*self.value)+int(Distance.unit)),
      ComparingOperator.at_most   : randrange(int(Distance.unit), self.value+1),
      ComparingOperator.exactly   : self.value
    }[self.comparing_operator]
    
# program entry
if __name__ == '__main__':
  cmdline = argparse.ArgumentParser(usage='usage: trace_generator.py -s scope -p pattern -l 10000', description='Generate a random trace with a specific length.')
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
  various_numbers = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
  # instantiate the scope and pattern
  scope = PropertyFactory.create_scope(args.ascope)
  pattern = PropertyFactory.create_pattern(args.apattern)

  for i in range(0,len(various_numbers)):
    RandomTraceGenerator.segments_number = various_numbers[i]
    generator = RandomTraceGenerator(args.id, length, scope, pattern)
    generator.generate_trace()
