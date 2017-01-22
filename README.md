# Package mxklabs

*TODO (installation, etc.)*

### Package mxklabs: Modules

| Module | Description |
|---|---|---|
| [mxklabs.dimacs](#mxklabs.dimacs) | A Python module for writing DIMACS files. |

# <a name="mxklabs.dimacs">Module mxklabs.dimacs
This Python package mxklabs.dimacs is for reading (and in future possibly writing) files in the [DIMACS](http://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html) format. This format is the 'de facto' standard for Boolean formulas in [SAT competitions](http://www.satcompetition.org/) and [SAT solvers](http://www.satlive.org/solvers/).

### Module mxklabs.dimacs: Example
```python
import mxklabs.dimacs

try:
  # Read the DIMACS file "simple.cnf".
  dimacs = mxklabs.dimacs.read(filename="simple.cnf")
  # Print some stats.
  print("num_vars=%d, num_clauses=%d" % (dimacs.num_vars, dimacs.num_clauses))
  # Iterate over clauses.
  for clause in dimacs.clauses:
    # Print them out.
    print clause
except mxklabs.dimacs.DimacsException e:
  # Report error.
  print e  
```

### Module mxklabs.dimacs: API

### mxklabs.dimacs

| Object | Type | Description |
|---|---|---|
| [mxklabs.dimacs.Dimacs](#mxklabs.dimacs.Dimacs) | 'class' | A class representing a Boolean formula (in DIMACS format). |
| [mxklabs.dimacs.DimacsException](#mxklabs.dimacs.DimacsException) | 'class' | A class representing an exception. |
| mxklabs.dimacs.read_from_file(file) | 'function' | Parses the content of the 'file' object (as specified by the file parameter) and returns an object of type '[mxklabs.dimacs.Dimacs](#mxklabs.dimacs.Dimacs)'. |
| mxklabs.dimacs.read_from_filename(filename) | 'function' | Opens a file (as specified by the filename parameter), parses its returns an object of type '[mxklabs.dimacs.Dimacs](#mxklabs.dimacs.Dimacs)'. |
| mxklabs.dimacs.read_from_string(string) | 'function' | Parses the string parameter and returns an object of type '[mxklabs.dimacs.Dimacs](#mxklabs.dimacs.Dimacs)'. |

## <a name="mxklabs.dimacs.Dimacs">Class mxklabs.dimacs.Dimacs</a>

| Object | Type | Description |
|---|---|---|
| num_vars | 'int' | The number of Boolean variables. |
| num_clauses | 'int' | The number of clauses. |
| clauses | 'list' of 'list' of 'int' | The clauses. | 

## <a name="mxklabs.dimacs.DimacsException">Class mxklabs.dimacs.DimacsException</a>

*Inherits from Exception.*

## Reading DIMACS input.

1. Reading from a file:

```python
import mxklabs.dimacs as dimacs
dimacs = dimacs.read_from_file('file1.cnf')
```
