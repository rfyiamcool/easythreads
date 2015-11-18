#项目名:
Easythreads

#Usage:
from easythreads import AsyncWorker

def task_a():
    print 'a..'    

def task_b(a,b,c):
    print 'b...'

pool = AsyncWorker(10)

pool.append(task_a)

pool.append(task_b,1,2,3)

pool.shutdown(block=False) 
    
