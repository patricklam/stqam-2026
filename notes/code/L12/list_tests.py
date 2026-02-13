# https://fsharpforfunandprofit.com/posts/property-based-testing-3/

from hypothesis import settings, Verbosity
from hypothesis import given, strategies as st

@given(st.integers())
def test_is_integer(n):
    assert isinstance(n, int)

@given(st.lists(st.integers()))
@settings(verbosity=Verbosity.verbose)
def map_identity_yields_self(xs):
    def id(x):
        return x
    assert list(map(id, xs)) == xs

def test_map_identity_yields_self():
    map_identity_yields_self()
test_map_identity_yields_self()

@given(st.lists(st.integers()))
def add_then_sort_eq_sort_then_add(sort_fn, xs):
    def add1(x):
        return x + 1
    result1 = list(map(add1, sort_fn(xs)))
    result2 = sort_fn(list(map(add1, xs)))
    assert result1 == result2

def test_add_then_sort():
    add_then_sort_eq_sort_then_add(sorted)

def edfhSort1(xs):
    return xs

@given(st.lists(st.integers()))
def min_value_then_sort_eq_sort_then_min_value(sort_fn, xs):
    append_then_sort = sort_fn(xs + [float('-inf')])
    sort_then_prepend = [float('-inf')] + sort_fn(xs)
    assert append_then_sort == sort_then_prepend

def test_min_value_then_sort_eq_sort_then_min_value():
    min_value_then_sort_eq_sort_then_min_value(sorted)

def edfhSort2(xs):
    if xs == []:
        return []
    if xs[-1] == float('-inf'):
        return [xs[-1]] + xs[:-1]
    else:
        return xs

@given(st.lists(st.integers()))
def negate_then_sort_eq_sort_then_negate_then_reverse(sort_fn, xs):
    def negate(x):
        return x * -1

    negate_then_sort = sort_fn(list(map(negate, xs)))
    sort_then_negate_then_reverse = list(reversed(list(map(negate, sort_fn(xs)))))
    assert negate_then_sort == sort_then_negate_then_reverse

def test_negate_then_sort_eq_sort_then_negate_then_reverse():
    negate_then_sort_eq_sort_then_negate_then_reverse(sorted)

def edfhSort3(xs):
    return []

@given(st.integers(), st.lists(st.integers()))
def append_then_reverse_eq_reverse_then_prepend(rev_fn, x, xs):
    append_then_reverse = list(rev_fn(xs + [x]))
    reverse_then_append = [x] + list(rev_fn(xs))
    assert append_then_reverse == reverse_then_append

def test_append_then_reverse_eq_reverse_then_prepend():
    append_then_reverse_eq_reverse_then_prepend(reversed)

def edfhReverse1(xs):
    return []

def edfhReverse2(xs):
    return xs

@given(st.lists(st.integers()))
def reverse_then_reverse_eq_original(rev_fn, xs):
    reverse_then_reverse = list(rev_fn(list(rev_fn(xs))))
    assert reverse_then_reverse == xs

def test_reverse_then_reverse_eq_original():
    reverse_then_reverse_eq_original(reversed)

@given(st.lists(st.text()))
def concat_elements_of_split_string_eq_original_string(xs):
    input_string = ",".join(xs)
    tokens = input_string.split(",")
    recombined_string = ",".join(tokens)
    assert input_string == recombined_string

def test_concat_elements_of_split_string_eq_original_string():
    concat_elements_of_split_string_eq_original_string()

#test_concat_elements_of_split_string_eq_original_string()

