simplex_grammar = """

    start: exp
         | exp "=" NUMBER          -> rhs_eq
         | exp "<=" NUMBER         -> rhs_ineq_less
         | exp ">=" NUMBER         -> rhs_ineq_more
         | "Min" NAME "=" exp      -> min_equation
         | "Max" NAME "=" exp      -> max_equation

    exp: exp vr
         | vr

    vr: "-" NUMBER NAME            -> neg
         | "+"? NUMBER NAME        -> pos
         | "+"? NAME               -> pos_single
         | "-" NAME                -> neg_single

    %import common.CNAME           -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""
