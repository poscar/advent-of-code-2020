import time

def timeit(f):
  def wrapped(*args, **kwargs):
    start = time.perf_counter()
    result = f(*args, **kwargs)
    print(f"{f.__name__} took: {time.perf_counter() - start}s")
    return result
  return wrapped