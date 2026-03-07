fn main() {
    println!("Hello, world!");
}

fn nth_rev(arr: &[i32], index: usize) -> Option<i32> {
    if index < arr.len() {
        let rev_index = arr.len() - index - 1;
        return Some(arr[rev_index]);
    }
    None
}

const N: usize = 5;

#[test]
#[cfg_attr(kani, kani::proof)]
fn check_rev() {
    bolero::check!()
        .with_type::<([i32; N], usize)>()
        .cloned()
        .for_each(|(arr, index)| {
            let x = nth_rev(&arr, index);
            if index < arr.len() {
                assert!(x.is_some());
            }
        });
}
