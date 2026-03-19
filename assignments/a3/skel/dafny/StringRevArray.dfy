predicate isReversed(s: array<char>, r: array<char>)
    reads s, r
    requires s.Length == r.Length
{
  true
}


method StringReverse(s: array<char>) returns (r: array<char>)
  requires s.Length > 0
  ensures s.Length == r.Length
  ensures isReversed(s, r)           // ensure r is correctly reversed
{
    r := new char[s.Length];
    var i := 0;
    var j := s.Length - 1;
    r[i] := s[j];
    i := i + 1;
    j := j - 1;
    while i < s.Length
    {
        r[i] := s[j];
        i := i + 1;
        j := j - 1;
    }
}
