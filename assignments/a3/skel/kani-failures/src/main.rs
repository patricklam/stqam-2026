fn foo() -> u32 {
}

#[cfg(kani)]
#[kani::proof]
fn proof_harness_divide_by_zero() -> u32 {
}

fn bar() -> usize {
}

#[cfg(kani)]
#[kani::proof]
fn proof_harness_array_out_of_bounds() -> i32 {
}

#[cfg(kani)]
#[kani::proof]
fn unwrap_on_none() -> i32 {
    let a:Option<i32> = Some(5);
}

fn main() {
}

