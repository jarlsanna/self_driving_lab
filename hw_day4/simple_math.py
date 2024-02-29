"""
A module for performing simple arithmetic operations and polynomial evaluations.

Functions:
----------
simple_add : function
    Computes the sum of two numbers.

simple_sub : function
    Computes the difference between two numbers.

simple_mult : function
    Computes the product of two numbers.

simple_div : function
    Computes the division of two numbers.

poly_first : function
    Evaluates a first-degree polynomial at a given point.

poly_second : function
    Evaluates a second-degree polynomial at a given point.

"""

def simple_add(a,b):
    return a+b

def simple_sub(a,b):
    return a-b

def simple_mult(a,b):
    return a*b

def simple_div(a,b):
    return a/b

def poly_first(x, a0, a1):
    return a0 + a1*x

def poly_second(x, a0, a1, a2):
    return poly_first(x, a0, a1) + a2*(x**2)

# Feel free to expand this list with more interesting mathematical operations...
# .....
