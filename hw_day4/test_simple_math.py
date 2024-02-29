import pytest
import simple_math as sm

@pytest.fixture
def substrate_a():
    a = 2
    return a

@pytest.fixture
def substrate_b():
    b = 6
    return b

@pytest.fixture
def x():
    return 5

def test_simple_add(substrate_a, substrate_b):
    assert sm.simple_add(substrate_a, substrate_b) == 8

def test_simple_subtract(substrate_a, substrate_b):
    result = sm.simple_sub(substrate_a, substrate_b)
    assert result == -4

def test_simple_mult(substrate_a, substrate_b):
    result = sm.simple_mult(substrate_a, substrate_b)
    assert result == 12

def test_simple_div(substrate_a, substrate_b):
    result = sm.simple_div(substrate_b, substrate_a)
    assert result == 3

def test_poly_first(substrate_a, substrate_b, x):
    result = sm.poly_first(x, substrate_a, substrate_b)
    assert result == 32

def test_poly_second(substrate_a, substrate_b, x):
    a2 = 3
    result = sm.poly_second(x, substrate_a, substrate_b, a2)
    assert result == 107