# thread_processor
Generate tasks for each argument in a list and execute them through a fixed number of threads

# Sample usage

<pre>
import logging
from thread_processor import ThreadProcessor

args = [(1,), (2,), (3,), (4,), (5,), (6,)]

def thread_func(arg):
    import time
    time.sleep(arg)
    if arg%2 == 0:
      raise Exception("Raising exception {}".format(arg))

tq = ThreadProcessor(
    thread_func=thread_func,
    thread_func_args_list=args,
    max_threads=2
    )
tq.start()
</pre>

# Output
<pre>
[INFO] (MainThread) Started Thread Name: 1 Args: (6,)
[INFO] (MainThread) Started Thread Name: 2 Args: (5,)
[INFO] (MainThread) Active Threads [Name: 1 Args: (6,), Name: 2 Args: (5,)]
[INFO] (MainThread) Started Thread Name: 3 Args: (4,)
[INFO] (MainThread) Started Thread Name: 4 Args: (3,)
[INFO] (MainThread) Active Threads [Name: 3 Args: (4,), Name: 4 Args: (3,)]
[INFO] (MainThread) Started Thread Name: 5 Args: (2,)
[INFO] (MainThread) Started Thread Name: 6 Args: (1,)
[INFO] (MainThread) Active Threads [Name: 5 Args: (2,), Name: 6 Args: (1,)]
[INFO] (MainThread) No more threads to create
[INFO] (MainThread) All threads complete
[INFO] (MainThread) Ran:6 Successful:3 Failed:3
[INFO] (MainThread) Failed threads: [Name: 1 Args: (6,), Name: 3 Args: (4,), Name: 5 Args: (2,)]
[INFO] (MainThread) Bye
</pre>
