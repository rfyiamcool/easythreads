from easythreads import AsyncWorker


def task_a():
    print 123
  
  
def task_b(n):
  for i in range(n):
    print 999
    

pool = AsyncWorker(10)


for _ in range(100) :
    pool.append(task_a)
  

for n in range(100): 
    pool.append(lambda : task_b(n))
  
pool.shutdown()
