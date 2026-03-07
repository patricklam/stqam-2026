method all_positive() returns (rv:array<int>)
	ensures forall k: int :: 0 <= k < rv.Length ==> 0 < rv[k]
{
	var arr := new int[2];
	arr[0] := 2;
	arr[1] := -3;
	return arr;
}

method Abs(x:int) returns (y:int) {
	if x < 0 {
		return -x;
	} else {
  	return x;
	}
}

method MultipleReturns(x:int, y:int) returns (more:int, less:int)
    ensures less < x
    ensures x < more
{
	more := x + y;
	less := x - y;
}

method AbsWithPostcondition(x:int) returns (y:int)
	ensures 0 < y
{
	if x < 0 {
		return -x;
	} else {
  	return x;
	}
}

method Max(a: int, b: int) returns (c: int)
	ensures c >= a && c >= b
{
	if a > b {
		return a;
	} else {
		return b;
	}
}

method m()
{
  var x, y, z: bool := 1, 2, true;
}

method TestAbsWithPostcondition(){
	var v := AbsWithPostcondition(3);
	assert 0 <= v;
}

method TestMax() {
	// ...
}

method TestAbs()
{
  var v := AbsWithPostcondition(3);
  assert 0 <= v;
  assert v == 3;
}

method NotAbs(x:int) returns (y:int)
ensures 0 <= y
{
  return 5;
}

method TestNotAbs(x:int) returns (y:int)
ensures 0 <= y
{
  var v := NotAbs(3);
  assert v == 3; // actually not true
}

method AbsBetterPostcondition(x:int) returns (y:int)
ensures 0 <= y
ensures 0 <= x ==> y == x
{
  if x < 0 {
    return -x;
  } else {
    return x;
  }
}

method TestAbsBetter(x:int) returns (y:int)
{
	var v := AbsBetterPostcondition(5);
	assert v == 5;
	var w := AbsBetterPostcondition(-2);
	assert w == 2;
}

method AbsFullPostcondition(x:int) returns (y:int)
ensures 0 <= y
ensures 0 <= x ==> y == x
ensures x < 0 ==> y == -x
{
  if x < 0 {
    return -x;
  } else {
    return x;
  }
}

method AbsAnotherPostcondition(x:int) returns (y:int)
	ensures 0 <= y && (y == x || y == -x)
{
  if x < 0 {
    return -x;
  } else {
    return x;
  }
}

method AbsOnlyNegative(x:int) returns (y:int)
	requires x < 0
	ensures y == -x
{
	return -x;
}
	
method AbsContrivedPreconditionOne(x:int) returns (y:int)
	// add a precondition so that the method verifies
	ensures 0 <= y
	ensures 0 <= x ==> y == x
	ensures x < 0 ==> y == -x
{
	y := x + 2;
}

method AbsContrivedPreconditionTwo(x:int) returns (y:int)
	requires false
	ensures 0 <= y
	ensures 0 <= x ==> y == x
	ensures x < 0 ==> y == -x
{
	y := x + 1;
}

function abs(x:int) : int
{
  if x < 0 then -x else x
}

method m2()
{
  assert abs(3) == 3;
}

function max(x:int, y:int) : int
{
	if x > y then x else y
}

method testMax()
{
	assert max(3, 5) == 5;
}

method AbsWithFunction(x:int) returns (y:int)
	ensures y==abs(x)
{
	return abs(x);
}  

method ComputeFib(n: nat) returns (b: nat)
//  ensures b == fib(n)
{
  // ...
}

method FirstLoop(n:nat) 
{
  var i := 0;
  while i < n
		invariant 0 <= i < n
  {
    i := i + 1;
  }
  assert i == n;
}

// Monday stop point

method AddByInc(n:nat, m:nat) returns (r:nat)
  ensures r == n + m
{
  r := n;
  var i := 0;
  while (i < m)
    invariant 0 <= i <= m;
    invariant r == n + i;
  {
    i := i + 1;
    r := r - 1;
  }
  assert (r == n + i && i == m);
  assert (r == n + m);
}

function fib(n:nat): nat
{
	if n == 0 then 0
	else if n == 1 then 1
	else fib(n-1) + fib(n-2)
}

method SimplerFib(n:nat) returns (b:nat)
	ensures b == fib(n)
{
	var i := 0;
	b := 0;
	var c := 1;
	while i < n
		invariant 0 <= i <= n
		invariant b == fib(i)
		invariant c == fib(i+1)
	{
		b, c := c, b + c;
		i := i + 1;
	}
}

method Decreases()
{
  var i := 20;
  while 0 < i
    invariant 0 <= i
    {
      i := i - 1;
    }
}

method Decreases2()
{
  var i, n := 0, 20;
  while i < n
    invariant 0 <= i <= n
    decreases n - i
    {
      i := i + 1;
    }
}

method Decreases3()
{
  var i, n := 0, 20;
  while i != n
    invariant 0 <= i <= n
    decreases n - i
    {
      i := i + 1;
    }
}

function fib2(n:nat): nat
  decreases n
{
  if n == 0 then 0
  else if n == 1 then 1
  else fib2(n-1) + fib2(n-2)
}

method FindPartialContract(a: array<int>, key:int) returns (index:int)
  // partial contract
  ensures 0 <= index ==> index < a.Length && a[index] == key
{
  // can you write code that satisfies this postcondition?
  // it can be done with one statement.
	return -1;
}

method WithQuantifier()
{
  assert forall k :: k < k + 1;
}

method Find(a: array<int>, key:int) returns (index:int)
  ensures 0 <= index ==> index < a.Length && a[index] == key
  ensures index < 0 ==> forall k :: 0 <= k < a.Length ==> a[k] != key
{
  index := 0;
  while index < a.Length
		invariant 0 <= index <= a.Length
		invariant forall k :: 0 <= k < index ==> a[k] != key
	{
    if a[index] == key {
      return;
    }
    index := index + 1;
  }
  index := -1;
}

method FindMax(a: array<int>) returns (maxIndex:int)
	requires a.Length >= 1
	ensures 0 <= maxIndex < a.Length && forall k :: 0 <= k < a.Length ==> a[maxIndex] >= a[k]
{
	maxIndex := 0;
	var i := 0;
  while i < a.Length
		invariant maxIndex < a.Length
		invariant 0 <= maxIndex <= i <= a.Length
		invariant forall k :: 0 <= k < i ==> a[maxIndex] >= a[k]
	{
		if a[i] > a[maxIndex] {
			maxIndex := i;
		}
		i := i + 1;
	}
}

predicate sorted(a: array<int>)
	reads a
{
  forall j, k :: 0 <= j < k < a.Length ==> a[j] <= a[k]
}

predicate sortedAndDistinct(a: array<int>)
	reads a
{
  forall j, k :: 0 <= j < k < a.Length ==> a[j] < a[k]
}

predicate sortedAndNotNull(a: array?<int>)
	reads a
{
  a != null && forall j, k :: 0 <= j < k < a.Length ==> a[j] < a[k]
}

method BinarySearch(a: array<int>, value: int) returns (index:int)
  requires 0 <= a.Length && sorted(a)
  ensures 0 <= index ==> index < a.Length && a[index] == value
  ensures index < 0 ==> forall k :: 0 <= k < a.Length ==> a[k] != value
{
  var low, high := 0, a.Length;
  while low < high
    invariant 0 <= low <= high <= a.Length
    invariant forall i ::
      0 <= i < a.Length && !(low <= i < high) ==> a[i] != value
  {   
      var mid := (low + high) / 2;
      if a[mid] < value {
        low := mid + 1;
      } else if value < a[mid] {
        high := mid;
      } else {
        return mid;
      }
  }
  return -1;
}

