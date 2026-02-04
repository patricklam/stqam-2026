# Code from The Fuzzing Book, https://www.fuzzingbook.org

def trace_options(frame, event, arg):
  if event != "call":
      return
  method_name = frame.f_code.co_name
  if method_name != "add_argument":
      return
  locals = frame.f_locals
  print(locals['args'])
