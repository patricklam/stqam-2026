method findMaxFrequency(v: array<int>) returns (maxElt:int , count:int)
  requires v != null && v.Length >= 1
  ensures countOcc (v,maxElt,v.Length ) == count
  ensures forall j :: 0 <= j < v.Length ==> countOcc(v, v[j], v.Length) <= count
{
  var i := 0;
  var freq := map [];
  while i < v.Length {
    if v[i] in freq {
      var prev_freq := freq[v[i]];
      freq := freq[v[i] := prev_freq + 1];
    } else {
      freq := freq [v[ i ]:= 1];
    }
    i := i + 1;
  }
  i := 0;
  maxElt := v[0];
  while i < v.Length {
    if freq[v[i]] > freq[maxElt] {
    maxElt := v[i]; }
  i := i + 1; }
  count := freq[maxElt];
}

function countOcc(v: array<int >, elt: int , n: nat) : nat {
  if n == 0 then 0 else
    countOcc(v,elt,n-1) + if v[n-1] == elt then 1 else 0
}
