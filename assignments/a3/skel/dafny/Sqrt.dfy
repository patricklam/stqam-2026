method SquareRoot1(N: nat) returns (r: nat)
  ensures r*r <= N < (r+1)*(r+1)
{
  r := 0;
  while (r+1)*(r+1) <= N
  {
    r := r+1;
  }
}

method SquareRoot2(N: nat) returns (r: nat)
  ensures r * r <= N < (r+1) * (r+1)
{
  r := 0;
  var sqr := (r+1) * (r+1);
  while sqr <= N
  {
    r := r + 1;
    sqr := sqr + 2 * r + 1;
  }
}
