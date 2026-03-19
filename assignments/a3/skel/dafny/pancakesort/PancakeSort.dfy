include "flip.dfy"
include "findmax.dfy"


method pancakeSort (a : array<int>)
  modifies a;
  ensures forall i, j :: 0 <= i <= j < a.Length ==> a[i] <= a[j];
{
  var curr_size := a.Length;
  while (curr_size > 1)
  {
    var mi := findMax (a, curr_size);
    if (mi != curr_size - 1)
    {
      flip (a, mi);
      flip (a, curr_size -1);
    }
    curr_size := curr_size - 1;
  }
}
