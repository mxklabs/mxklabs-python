import collections
import decimal
import functools
import multiprocessing as mp
import timeit

import mxklabs

class RsaEvalResult:

  def __init__(self, results):
    self._results = results

  def get_fields(self):
    return functools.reduce(lambda a, b: a.union(b), [set(r.keys()) for r in self._results], set())

  def get_values(self, field):
    return [r[field] if field in r else None for r in self._results]

class RsaEvalTool:

  DEFAULT_TIMEOUT = 10.0

  def __init__(self):
    pass

  def evaluate(self, fun, benchmarks=None, timeout=DEFAULT_TIMEOUT, verbose=False):
    """ Evaluate a factorisation function. """
    results = []
    if benchmarks is None:
      benchmarks = mxklabs.rsa.RsaBenchmarkRepository.all()
    for benchmark in benchmarks:
      try:
        result = self.evaluate_benchmark(fun, benchmark, float(timeout))
        if verbose:
          self._print_result(result)
        results.append(result)
      except TimeoutError:
        print(f"[TIME OUT AFTER {int(timeout):d}s]")
        break
    return RsaEvalResult(results)

  def evaluate_benchmark(self, fun, benchmark, timeout=DEFAULT_TIMEOUT, verbose=False):
    """ Run a function with prototype fun(modulus, callback)
        in a multiprocess which times out if it takes too long.
    """
    modulus = benchmark.prime1 * benchmark.prime2
    queue = mp.Queue()
    event = mp.Event()
    def callback(result, stats):
      queue.put((result, stats))
      event.set()
    process = mp.Process(target=fun, args=(modulus, callback))
    start = timeit.default_timer()
    process.start()

    fun_terminated = False

    while timeit.default_timer() - start <= timeout:
      if event.is_set():
        fun_terminated = True
        break
      event.wait(timeout=1.0)  # Just to avoid hogging the CPU

    if fun_terminated:
      process.join()
      end = timeit.default_timer()

      assert not queue.empty()
      res, stats = queue.get()

      assert(modulus % res == 0)
      assert(res == benchmark.prime1 or res == benchmark.prime2)

      log = collections.OrderedDict()
      log['benchmark-id'] = benchmark.id
      log['modulus'] = modulus
      log['modulus-sqrt'] = mxklabs.rsa.RsaUtils.get_rounded_sqrt(modulus, decimal.ROUND_FLOOR)
      log['modulus-bit-length'] = modulus.bit_length()
      log['run-time'] = end - start

      for key, value in stats.items():
        log[key] = value

      return log
    else:
      process.terminate()
      process.join()

      raise TimeoutError(f"Function timed out on benchmark {benchmark.id} after {int(timeout):d}s (increase the timeout using the timeout parameter)")

  def _print_result(self, result):
    print('-' * 80)
    for key, value in result.items():
      if type(value) is int:
        print(f'  {key}={value:d}')
      elif type(value) is float:
        print(f'  {key}={value:.03f}')
      else:
        print(f'  {key}={value}')