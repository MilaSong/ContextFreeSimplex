# Simplex method solver
Context-free grammars based optimization equation parser and simplex method 
solver. Mainly used for university studies.

## Input
The input file can be given under the argument `--infile` while running the file
in terminal. The argument is not required. If no input file is given, the 
program uses default filename `equations.txt`. The example is given below:
```
python simplex -infile data.txt
```

## Input file syntax
The first line is the equation that will be optimized. The optimisation 
arguments can be either `Min` or `Max`. The rest of the lines are constraints
of the optimisation task. The example of the optimisation task is given below:

```
Max fx = 30x1 + 20x2
2x1 + x2 <= 10
x1 + x2 >= 8
x1 = 4
```

## Output
The output is based on scipy [linprog](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-simplex.html) 
library results. The only additional variable is the `solution` variable, which
is simply the optimal solution of the optimisation equation:
`
fx = 30 * 4 + 20 * 2 = 160.
`

The example of the output is given below:

```
     con: array([0.])
     fun: -160.0
 message: 'Optimization terminated successfully.'
     nit: 1
   slack: array([ 0., 14.])
  status: 0
 success: True
       x: array([4., 2.])
solution: 160.0
```