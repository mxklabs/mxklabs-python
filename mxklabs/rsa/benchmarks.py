import collections

import mxklabs.rsa.benchmarks_gen as benchmarks_gen

class RsaBenchmark:
  def __init__(self, bit_length, id, prime1, prime2):
    self.id = id
    self.modulus = prime1 * prime2
    self.prime1 = prime1
    self.prime2 = prime2
    self.bit_length = self.modulus.bit_length()
    assert(self.prime1 <= self.prime2)
    assert(self.modulus.bit_length() == bit_length)
    assert(self.modulus.bit_length() == 2*self.prime1.bit_length())
    assert(self.modulus.bit_length() == 2*self.prime2.bit_length())

class RsaBenchmarkRepository:

  @staticmethod
  def all():
    """ Yield all available benchmarks. """
    benchmarks = [RsaBenchmark(**kwargs) for kwargs in benchmarks_gen.RSA_BENCHMARKS]
    for benchmark in benchmarks:
      yield benchmark

  @staticmethod
  def sharded(max_benchmarks_for_each_bit_length=1):
    """ Only yield up to a specified maximum of benchmarks for each bit length. """
    benchmarks = [RsaBenchmark(**kwargs) for kwargs in benchmarks_gen.RSA_BENCHMARKS]
    last_bit_length = 0
    count = 0
    for benchmark in benchmarks:
      if benchmark.bit_length == last_bit_length:
        if max_benchmarks_for_each_bit_length is not None and \
          count >= max_benchmarks_for_each_bit_length:
          continue
        else:
          count += 1
          yield benchmark
      else:
        last_bit_length = benchmark.bit_length
        count = 1
        yield benchmark
