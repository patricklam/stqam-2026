fn max(x:u32, y:u32) -> u32 {
    if x < y { return y; } else { return x; }
}

fn slow_max(a:u32, b:u32) -> u32 {
    let mut z = 0;
    let mut x = a;
    let mut y = b;

    while z < x && z < y {
        z = z + 1;
        x = x - 1;
        y = y - 1;
    }

    if x <= y {
        return b;
    } else {
        return a;
    }
}

#[test]
fn test_slow_max() {
    let r = slow_max(3, 5);
    assert_eq!(r, 5);
}

#[cfg(kani)]
#[kani::proof]
#[kani::unwind(10)]
fn proof_harness_slow_max_a() {
    // fill in this proof harness
    let a = 2;
    let b = 1;
    kani::assume(a >= b);
    // ...
}
