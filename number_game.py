'''*-----------------------------------------------------------------------*---
                                                          Authors: Jason Ma
                                                          Date   : Feb 06, 2018
    File Name  : number_game.py
    Description: Determines whether or not a set of numbers can produce another
                 number using an augmented set of operations.
---*-----------------------------------------------------------------------*'''

import sys
import queue
from threading import Thread

import time

'''----------------------------------------------------------------------------
  Config variables
----------------------------------------------------------------------------'''
NUM_THREADS = 1
TARGET = 2018

MAX_VAL = 20000           #does not hash values above this
FIND_ONE = False          #stops after finding a single solution
FULL_COMPUTATION = False  #whether to use hashing or fully compute all combs
MANUAL = True             #manual mode, uses manual_override method
RANDOM = False            #random mode, uses random_override method

'''----------------------------------------------------------------------------
  Conditional imports
----------------------------------------------------------------------------'''
if RANDOM:
  import random

'''----------------------------------------------------------------------------
  Global variables
----------------------------------------------------------------------------'''
q = queue.Queue()
op = ['+',   '*',   '-',   '/',   '>',   '<',   '^>',   '^<',
      'f+',  'f*',  'f-',  'f/',  'f>',  'f<',  'f^>',  'f^<',
      '+f',  '*f',  '-f',  '/f',  '>f',  '<f',  '^>f',  '^<f',
      'f+f', 'f*f', 'f-f', 'f/f', 'f>f', 'f<f', 'f^>f', 'f^<f']

'''[Worker]--------------------------------------------------------------------
  Works on queue until it receives a signal to stop (nothing else to process)
----------------------------------------------------------------------------'''
class Worker(Thread):
  total = 0
  num_sol = 0
  seen = dict()
  found = False

  '''[__init__]----------------------------------------------------------------
    Initializes thread.

    tid - thread id
  --------------------------------------------------------------------------'''
  def __init__(self, tid):
    self.id = tid
    self.go = True
    Thread.__init__(self)

  '''[run]---------------------------------------------------------------------
    Run thread. 
  --------------------------------------------------------------------------'''
  def run(self):
    print('[{0:{width}}] - Running'.format(self.id, width=4))
    while self.go:
      try:
        state = q.get(timeout=5)
      except queue.Empty:
        #print('[{0:{width}}] - Empty. Trying again'.format(self.id, width=4))
        continue

      if state is None:
        #print('[{0:{width}}] - Stopping'.format(self.id, width=4))
        q.task_done()
        break

      if (FIND_ONE and Worker.found):
        q.task_done()
        continue

      # could assign processes to handle certain state lengths
      '''
      if self.id > 2 and self.id <= 4 and len(state) != 4:
        q.put(state)
        q.task_done()
        continue
      elif self.id > 4 and self.id <= 14 and len(state) != 3:
        q.put(state)
        q.task_done()
        continue
      '''

      # hash tuples using dict to avoid repetitive computations
      if not FULL_COMPUTATION and len(state) >= 3:
        nums = state[:len(state) - 1]
        nums.sort()
        t = tuple(nums)

        #print(nums)
        if t in Worker.seen:
          q.task_done()
          continue
        else:
          Worker.seen[t] = 0
      # determine if solution was found
      elif len(state) == 2:
        if state[0] == TARGET:
          print('[{0:{width}}] - {1}={2}'.format(self.id, state[0], state[1], width=4))
          Worker.num_sol += 1
          Worker.found = True
        #print('[{0:{width}}] - Bad Res: {1}={2}'.format(self.id, state[0], state[1], width=4))
        Worker.total += 1
        q.task_done()
        continue
      
      #print('[{0:{width}}] - {1}'.format(self.id, state, width=4))
      # process element
      process_state(state)

      #add(state)
      #sub(state)
      #mult(state)
      #div(state)

      # when successful, mark task as done
      q.task_done()

    return

  '''[end_callback]------------------------------------------------------------
    Ends thread. 
  --------------------------------------------------------------------------'''
  def end_callback(self):
    print('[{0:{width}}] - Stopping. Received Callback'.format(self.id, width=4))
    self.go = False
# rules for states
# - state cannot be float or <= 0

'''[process_state]-------------------------------------------------------------
  Choose all combinations of 2 numbers to combine and form new states based on
  results. 

  state - input state consisting of numbers followed by operation string
----------------------------------------------------------------------------'''
def process_state(state):
  #permute 2 elements, then perform all ops on them
  for i in range(len(state) - 2):
    for j in range(i + 1, len(state) - 1):
      l = process_nums(state[i], state[j])

      for k in range(len(l)):
        if l[k] <= 0 or l[k] > MAX_VAL:
          continue

        new_state = []
        new_state.extend(state)
        new_state[i] = l[k]

        if str(state[i]) + op[k] + str(state[j]) == "1/1":
          print(k, l[k])
        del new_state[j]
        new_state[-1] += str(state[i]) + op[k] + str(state[j]) + ' '
        q.put(new_state)
        #print(i, j, new_state)

'''[process_nums]--------------------------------------------------------------
  Form and return list from all operations on input numbers.

  i - first num
  j - second num
----------------------------------------------------------------------------'''
def process_nums(i, j):
  l = []

  # determine flips of i and j
  if i % 10 != 0:
    fi = int(str(i)[::-1])
  else:
    fi = i

  if j % 10 != 0:
    fj = int(str(j)[::-1])
  else:
    fj = j

  # no flips
  l.extend(proc_num_helper(i, j))

  # flipped i
  if fi != i:
    l.extend(proc_num_helper(fi, j))
  else:
    l.extend([0 for i in range(8)])

  # flipped j
  if fj != j:
    l.extend(proc_num_helper(i, fj))
  else:
    l.extend([0 for i in range(8)])

  # both i and j flipped
  if fi != i and fj != j:
    l.extend(proc_num_helper(fi, fj))
  else:
    l.extend([0 for i in range(8)])

  return l

'''[proc_num_helper]-----------------------------------------------------------
  Does a single set of operations on numbers without flips

  i - first number
  j - second number
----------------------------------------------------------------------------'''
def proc_num_helper(i, j):
  l = []

  # add and mult
  l.append(i + j)
  l.append(i * j)

  # sub
  if i > j:
    l.append(i - j)
  else:
    l.append(j - i)

  # div
  if i > j and i % j == 0:
    l.append(i // j)
  elif j > i and j % i == 0:
    l.append(j // i)
  else: 
    l.append(0)

  # concats
  l.append(int(str(i) + str(j)))
  l.append(int(str(j) + str(i)))

  # exponents
  if j <= 5:
    l.append(i**j)
  else:
    l.append(0)

  if i <= 5:
    l.append(j**i)
  else:
    l.append(0)

  '''
  if i < j:
    log_f = log(i, j)
  elif j < i:
    log_f = log(j, i)
  else:
    l.append(0)
  '''

  return l

def random_override():

  total_sols = 0
  '''
  for i in range(100):
    base_state = []
    for i in range(5):
      base_state.append(random.randint(1, 13))
    base_state.append('')
  '''

  #deck simulation
  for i in range(10):
    deck = []
    sets = 0

    for i in range(1, 14):
      deck.extend([i for j in range(4)])

    while len(deck) > 0:
      base_state = []

      print(deck)

      if len(deck) == 12 or len(deck) == 6:
        for i in range(6):
          index = random.randint(0, len(deck) - 1)
          base_state.append(deck[index])
          del deck[index]
      else:
        for i in range(5):
          index = random.randint(0, len(deck) - 1)
          base_state.append(deck[index])
          del deck[index]

      base_state.append('')
      print(base_state)
      q.put(base_state)

      q.join()
      print('[rand] Num Sols:' + str(Worker.num_sol))

      if Worker.num_sol == 0:
        print('[rand] Readding cards to deck')
        base_state.pop()
        deck.extend(base_state)

      total_sols += Worker.num_sol

      Worker.num_sol = 0
      Worker.seen = {}
      Worker.found = False
      sets += 1

    print("[rand] Total sols:" + str(total_sols))

'''[manual_override]-----------------------------------------------------------
  Runs when manual parameter is set to true. Should initialize queue.
----------------------------------------------------------------------------'''
def manual_override():
  print('[manual] Ready for input:')
  input_str = []
  while input_str != ['q']:
    try:
      input_str = sys.stdin.readline()
      input_str = input_str.strip().split(' ')
      for i in range(len(input_str)):
        input_str[i] = int(input_str[i])
    except KeyboardInterrupt:
      break
    except:
      print('[manual] Invalid input.')
      continue
    input_str.append('')
    q.put(input_str)
    q.join()
    print('[main] Sols: ' + str(Worker.num_sol) + '\tP: ' + str(Worker.total))
    Worker.total = 0
    Worker.num_sol = 0
    Worker.seen = {}
    Worker.found = False
  
  print('[manual] Ending')
  #q.put([3, 5, 6, 11, 12, ''])

'''[end_all_threads]-----------------------------------------------------------
  Sends end_callback to all threads in list of threads

  threads - list of threads
----------------------------------------------------------------------------'''
def end_all_threads(threads):
  print('[main] Ending program.')

  for thread in threads:
    thread.end_callback()

  print('[main] Processed: ' + str(Worker.total) + ' combinations')
  sys.exit(1)

'''[main]----------------------------------------------------------------------
  Initialize queue, start threads, then block until everything is joined. Also
  handles signals like keyboard interrupt.
----------------------------------------------------------------------------'''
if __name__ == '__main__':
  try:
    num_threads = NUM_THREADS
    base_state = []
    threads = []

    # normal stuff
    if not MANUAL and not RANDOM:
      base_nums = []
      for i in range(1, len(sys.argv)):
        base_nums.append(int(sys.argv[i]))
      
      if not base_nums:
        print('[main] USAGE: python3 number_game.py [numbers]')
        print('[main] Nothing to process. Exiting')
        sys.exit()

      # add starting states to queue
      base_state.extend(base_nums)
      base_state.append('')
      q.put(base_state)
    elif MANUAL:
      '''
      print('[main] Creating ' + str(num_threads) + ' threads')

      for i in range(num_threads):
        t = Worker(i)
        #t.daemon = True
        threads.append(t)

      for t in threads:
        #start threads
        t.start()

      print('[main] Waiting for threads to finish')

      manual_override()
      '''

      '''
      print('[main] Ending threads')
      print('[main] Num Sols:' + str(Worker.num_sol))
      print('[main] Processing Complete: ' + str(Worker.total) + ' combinations')

      # stop threads when nothing else to process
      for t in threads:
        q.put(None)
      '''
      pass

    elif RANDOM:
      pass
    
    print('[main] Creating ' + str(num_threads) + ' threads')
    for i in range(num_threads):
      t = Worker(i)
      #t.daemon = True
      threads.append(t)

    for t in threads:
      #start threads
      t.start()

    print('[main] Waiting for threads to finish')
    
    if MANUAL:
      manual_override()
      '''
      max_sol = 0
      best_set = []
      for n1 in range(1, 14):
        for n2 in range(1, 14):
          for n3 in range(1, 14):
            for n4 in range(1, 14):
              for n5 in range(1, 14):
                base_nums = [n1, n2, n3, n4, n5, '']
                Worker.num_sol = 0
                Worker.seen = dict()

                q.put(base_nums)

                q.join()

                print(n1, n2, n3, n4, n5, Worker.num_sol)

                if Worker.num_sol > max_sol:
                  max_sol = Worker.num_sol
                  best_set = base_nums

      print('[main] Best set: ', best_set)
      '''
    elif RANDOM:
      random_override()
    else:
      q.join()
    print('[main] Ending threads')
    print('[main] Num Sols:' + str(Worker.num_sol))
    print('[main] Processing Complete: ' + str(Worker.total) + ' combinations')

    # stop threads when nothing else to process
    for t in threads:
      q.put(None)

    # wait for all threads to terminate
    for t in threads:
      t.join()
  except KeyboardInterrupt:
    print('\n[main] Ctrl+c received')
    end_all_threads(threads)

