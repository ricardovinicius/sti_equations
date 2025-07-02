"""
This module implements a wrapper of mathsteps library in /ext/js/
"""
import subprocess
import json
from sympy import *

MATHSTEPS_LIBRARY_PATH = './ext/js/mathsteps/index.js'

def get_equation_solve_steps(equation: str):
    result = subprocess.run(["node", f"{MATHSTEPS_LIBRARY_PATH}", f"{equation}"], capture_output=True, text=True)

    try:
        result_json = json.loads(result.stdout)
    except json.decoder.JSONDecodeError:
        result_json = None
        print("Error loading steps return")

    return result_json

def get_equation_solution(equation: str, variable: str):
    x = symbols(variable)
    lhs_str, rhs_str = equation.split("=")
    lhs = sympify(lhs_str)
    rhs = sympify(rhs_str)

    eq = Eq(lhs, rhs)

    res = solve(eq, x)

    if res:
        return float(res[0])
    return None


if __name__ == "__main__":
    print(get_equation_solve_steps("2*x + 3 = 7"))
    print(get_equation_solution("2*x + 3 = 7", 'x'))

