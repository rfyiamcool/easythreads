#项目名:
easythreads
使用threading实现了一个线程池,使用方法很是简单,我们只需要把执行的函数塞入线程池里就可以了.

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
    
