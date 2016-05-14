from time import sleep
from multiprocessing import Pool

def start_func_for_processes(n):
  sleep(0.5)
  result_sent_back_to_parent = n*n
  return result_sent_back_to_parent

if __name__ == '__main__':
  with Pool(processes=5) as p:
    results = p.map(start_func_for_processes, range(200), chunksize=10)
  print results
