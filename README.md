## <a name="mxklabs.dimacs">Module mxklabs.dimacs
This Python package mxklabs.dimacs is for reading (and in future possibly writing) files in the [DIMACS](http://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html) format. This format is the 'de facto' standard for Boolean formulas in [SAT competitions](http://www.satcompetition.org/) and [SAT solvers](http://www.satlive.org/solvers/).

### Example

Read a DIMACS file named "simple.cnf":
```python
import sys
import mxklabs.dimacs     

if __name__ == "__main__":
  ARGV_LEN = len(sys.argv)
  if ARGV_LEN == 2:
    try:
      # Read the DIMACS file "simple.cnf".
      dimacs = mxklabs.dimacs.read(filename=sys.argv[1])
      # Print some stats.
      print("num_vars=%d, num_clauses=%d" % (dimacs.num_vars, dimacs.num_clauses))
      # Iterate over clauses.
      for clause in dimacs.clauses:
        # Print them out.
        print clause

    except Exception as e:
      # Report error.
      print e
  else:
    if ARGV_LEN > 0:
      print("usage error: {} <file>".format(sys.argv[0]))
    else:
      print("usage error")
```
### API Summary

| Object | Type |
|---|---|
| [`mxklabs.dimacs.read`](#mxklabs.dimacs.read) [[`link`](#mxklabs.dimacs.read)] | `function` |
| [`mxklabs.dimacs.Dimacs`](#mxklabs.dimacs.Dimacs) [[`link`](#mxklabs.dimacs.Dimacs)] | `class` | 

#### <a name="mxklabs.dimacs.read"></a> `mxklabs.dimacs.read(file=None, filename=None, string=None)`

This function parses DIMACS input and returns a [`mxklabs.dimacs.Dimacs`](#mxklabs.dimacs.Dimacs) object. Input can be either:

1. an open [`file`](https://docs.python.org/2/library/stdtypes.html#file-objects) object (using the `file` parameter), 
2. a filename (using the `filename` parameter) or
3. an input string (using the `string` parameter).

In case of any errors the function will raise an [exception](https://docs.python.org/3/library/exceptions.html#Exception).

#### <a name="mxklabs.dimacs.Dimacs"></a> `mxklabs.dimacs.Dimacs`

| Object | Type | Description |
|---|---|---|
| num_vars | 'int' | The number of Boolean variables. |
| num_clauses | 'int' | The number of clauses. |
| clauses | 'list' of 'list' of 'int' | The clauses. | 


