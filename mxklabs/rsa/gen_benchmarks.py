import miller_rabin
import random

num_benchmarks_per_bits = 6

def get_prime_in_range(lb, ub):
  while True:
    c = random.randint(lb, ub)

    if c % 2 == 0:
      c += 1

    for p in range(c, ub, 2):
      if miller_rabin.miller_rabin(p, 100):
        return p

with open('benchmarks_gen.py', 'w') as f:

  f.write('RSA_BENCHMARKS = [\n')

  for modulus_bits in range(8, 2050, 2):

    for sample_index in range(num_benchmarks_per_bits):
      assert(modulus_bits % 2 == 0)
      prime_lb = 2**(modulus_bits//2)*3//4
      prime_ub = 2**(modulus_bits//2)-1

      prime1 = get_prime_in_range(prime_lb, prime_ub)
      prime2 = get_prime_in_range(prime_lb, prime_ub)

      assert(prime1.bit_length() == modulus_bits//2)
      assert(prime2.bit_length() == modulus_bits//2)
      assert((prime1*prime2).bit_length() == modulus_bits)

      if prime1 > prime2:
        tmp = prime2
        prime2 = prime1
        prime1 = tmp

      f.write(f"  {{ 'bit_length':{modulus_bits}, 'id':'#{modulus_bits}.{sample_index}', 'prime1':{prime1}, 'prime2':{prime2} }}, # {modulus_bits} bit modulus, {modulus_bits//2}-bit primes\n")

  f.write(']\n')