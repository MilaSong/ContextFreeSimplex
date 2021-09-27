import argparse
import numpy as np

from scipy.optimize import linprog
from lark import Lark, Transformer, v_args
from grammar import simplex_grammar

parser = argparse.ArgumentParser()
parser.add_argument('--infile', type=str, required=False)
args = parser.parse_args()
filename = args.infile if args.infile else "equations.txt"

with open(filename, "r") as f:
    eqs = f.readlines()


eqs = [eq.strip() for eq in eqs]
main_eq = eqs.pop(0)


def missing_elements(seq):
    """ Find the missing elements in the index sequence """
    start, end = min(main_index), max(main_index)
    return sorted(set(range(start, end + 1)).difference(seq))


@v_args(inline=True)
class SimplexParseTree(Transformer):
    def __init__(self):
        self.eq_coefs = []
        self.ineq_coefs = []
        self.coefs = []
        self.unknowns = []
        self.rhs_eqc = ''
        self.rhs_ineqc = ''

    def min_equation(self, value1, value2):
        self.eq_type = 'Min'
        return value1, value2

    def max_equation(self, value1, value2):
        self.eq_type = 'Max'
        self.coefs = np.array(self.coefs)*(-1)
        return value1, value2

    def rhs_eq(self, value1, value2):
        self.rhs_eqc = value2
        self.eq_coefs = self.coefs.copy()
        return value1, value2

    def rhs_ineq_less(self, value1, value2):
        self.rhs_ineqc = value2
        self.ineq_coefs = self.coefs.copy()
        return value1, value2

    def rhs_ineq_more(self, value1, value2):
        self.rhs_ineqc = value2
        self.ineq_coefs = list(np.array(self.coefs)*(-1))
        return value1, value2

    def pos(self, value1, value2):
        self.coefs.append(float(value1))
        index = value2.replace("x", "")
        self.unknowns.append(int(index))
        return value1, value2

    def neg(self, value1, value2):
        self.coefs.append(float(value1)*(-1))
        index = value2.replace("x", "")
        self.unknowns.append(int(index))
        return value1, value2

    def pos_single(self, value1):
        self.coefs.append(float(1))
        index = value1.replace("x", "")
        self.unknowns.append(int(index))
        return value1

    def neg_single(self, value1):
        self.coefs.append(float(-1))
        index = value1.replace("x", "")
        self.unknowns.append(int(index))
        return value1


mainobj = SimplexParseTree()
simplex_parser = Lark(simplex_grammar, parser='lalr', transformer=mainobj)
simplex = simplex_parser.parse
simplex(main_eq)
obj = mainobj.coefs
main_index = mainobj.unknowns
main_type = mainobj.eq_type


lhs_ineq = []
rhs_ineq = []
rhs_eqls = []
lhs_eqls = []

for eq in eqs:
    parserobj = SimplexParseTree()
    simplex_parser = Lark(simplex_grammar, parser='lalr', transformer=parserobj)
    simplex = simplex_parser.parse
    simplex(eq)

    eqc = parserobj.eq_coefs
    ineqc = parserobj.ineq_coefs
    missing = missing_elements(parserobj.unknowns)
    for el in missing:
        if len(eqc) > 0:
            eqc.insert(el-1,0)
        if len(ineqc) > 0:
            ineqc.insert(el-1,0)

    if parserobj.rhs_ineqc != '':
        rhs_ineq.append(parserobj.rhs_ineqc)
    if parserobj.rhs_eqc != '':
        rhs_eqls.append(parserobj.rhs_eqc)
    if len(ineqc) > 0:
        lhs_ineq.append(ineqc)
    if len(eqc) > 0:
        lhs_eqls.append(eqc)


bnd = []
for i in main_index:
    bnd.append((0, float("inf")))


if len(lhs_eqls) < 1:
    opt = linprog(c=obj,
                  A_ub=lhs_ineq,
                  b_ub=rhs_ineq,
                  bounds=bnd,
                  method="revised simplex")
else:
    opt = linprog(c=obj,
                  A_ub=lhs_ineq,
                  b_ub=rhs_ineq,
                  A_eq=lhs_eqls,
                  b_eq=rhs_eqls,
                  bounds=bnd,
                  method="revised simplex")


z = sum(obj*(-1)*opt.x) if main_type == 'Max' else sum(obj*opt.x)


print(opt)
print(f"solution: {z}")
