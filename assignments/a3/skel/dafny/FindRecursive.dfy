method Find(B:array<int>, target:int, i:int) returns (ind:int)
{
  if B[i] == target {
    ind := i;
  } else {
    ind := Find(B, target, i-1); 
  }
}
