  bool SlowPathCheck(int shadow_value, char * addr, int sz) {
    int last_accessed_byte = (long)(addr + sz - 1) % 8;
    return (last_accessed_byte >= shadow_value);
  }
