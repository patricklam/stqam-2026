# adapted from https://www.geeksforgeeks.org/python/run-length-encoding-python/ 
def run_length_encoding_mutant2(inpt):
  """
  Issue  python -m doctest rle.py  to run the doctests.

  >>> print(run_length_encoding('aaabb'))
  a3b2
  """
  output = ''
  count = 1

  if len(inpt) >= 2 and inpt[0] != inpt[1]:
    output += inpt[0] + '1'
    inpt = inpt[1:]

  for i in range(1, len(inpt)):
      if inpt[i] == inpt[i - 1]: 
          count += 1 
      else:
          output += inpt[i - 1] + str(count)  
          count = 1  
          
  output += inpt[i - 1] + str(count)

  return output 
