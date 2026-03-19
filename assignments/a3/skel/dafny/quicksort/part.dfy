// Students have reported that if the effective path name for preds.dfy is too long, the include 
// won't work. This might happen for OneDrive for instance.
include "preds.dfy"

// You can make changes to this specification-only method, but you can't execute it.
method choose(l:nat, u:nat) returns (rv: nat)
  requires l <= u
  ensures l <= rv <= u
{ rv := *; assume {:axiom} (l <= rv <= u); }

method partition(a:array<int>, l:nat, u:nat) returns (pivot:int)
  modifies a
  requires l <= u < a.Length
  requires l>0 ==> partitioned(a, 0, l-1, l, u)
  requires u+1 <= a.Length -1 ==> partitioned(a, l, u, u+1, a.Length-1)

  ensures l <= pivot <= u

  ensures l > 0 ==> beq(old(a[..]), a[..], 0, l-1)
  ensures l > 0 ==> partitioned(a, 0, l-1, l, u)

  ensures u < a.Length-1 ==> beq(old(a[..]), a[..], u+1, a.Length - 1)
  ensures u < a.Length - 1 ==> partitioned(a, l, u, u+1, a.Length-1)

  ensures pivot > l ==> partitioned(a, l, pivot-1, pivot, pivot)
  ensures pivot < u ==> partitioned(a, pivot, pivot, pivot+1, u)
{
  var pi := choose(l, u);
  var pv := a[pi];

  a[pi] := a[u];
  a[u] := pv;

  var i:int := l - 1;
  var j := l;
  while (j < u)
    // MISSING INVARIANT
  {
    if (a[j] <= pv)
    {
      i := i + 1;
      var t := a[i];
      a[i] := a[j];
      a[j] := t;
    }
    j := j + 1;
  }

  pivot := i + 1;
  var t := a[pivot];
  a[pivot] := a[u];
  a[u] := t;
}
