import collections

RsaBenchmark = collections.namedtuple("Benchmark", ['id', 'modulus', 'prime1', 'prime2'])

class RsaBenchmarkRepository:

  def __init__(self):
    """ Constructor. """
    self._index = 0
    self._benchmarks = [
      self._bake_benchmark(id='#8.0',  prime1=11, prime2=13), # 8 bit modulus, 4-bit primes
      self._bake_benchmark(id='#10.0', prime1=19, prime2=29), # 10 bit modulus, 5-bit primes
      self._bake_benchmark(id='#12.0', prime1=47, prime2=61), # 12 bit modulus, 6-bit primes
      self._bake_benchmark(id='#14.0', prime1=103, prime2=113), # 14 bit modulus, 7-bit primes
      self._bake_benchmark(id='#16.0', prime1=487, prime2=509), # 18 bit modulus, 9-bit primes
      self._bake_benchmark(id='#20.0', prime1=787, prime2=757), # 20 bit modulus, 10-bit primes
      self._bake_benchmark(id='#22.0', prime1=1531, prime2=1621), # 22 bit modulus, 11-bit primes
      self._bake_benchmark(id='#24.0', prime1=2753, prime2=3931), # 24 bit modulus, 12-bit primes
      self._bake_benchmark(id='#26.0', prime1=3917, prime2=3779), # 26 bit modulus, 13-bit primes
      self._bake_benchmark(id='#28.0', prime1=7247, prime2=6779), # 28 bit modulus, 14-bit primes
      self._bake_benchmark(id='#30.0', prime1=15643, prime2=15787), # 30 bit modulus, 15-bit primes
      self._bake_benchmark(id='#32.0', prime1=58537, prime2=57881), # 32-bit modulus, 16-bit primes
      # TODO
      self._bake_benchmark(id='#64.0', prime1=3665034161, prime2=4080306821), # 64-bit modulus, 32-bit primes
    ]

  def __iter__(self):
    """ Act as an iterator over the benchmarks. """
    for benchmark in self._benchmarks:
      yield benchmark

  def _bake_benchmark(self, id, prime1, prime2):
    """ Internal method so we can add a modulus. """
    if prime1 > prime2:
      return self._bake_benchmark(id, prime2, prime1)
    return RsaBenchmark(id=id, modulus=prime1*prime2, prime1=prime1, prime2=prime2)
