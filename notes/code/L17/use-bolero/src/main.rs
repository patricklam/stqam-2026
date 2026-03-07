fn main() {
    println!("Hello, world!");
}

fn update_account_balance(current_balance: i32, amount: i32) -> i32 {
    return current_balance + amount;
}

fn balance_update_is_correct(current_balance: i32, amount: i32, new_balance: i32) -> bool {
    // more generally: checks that the transaction was carried out correctly, and may include other properties as well, for example that no overflow occurred, there was enough balance for a withdrawal, etc.
    return current_balance + amount == new_balance;
}

#[test]
fn test_update_account_balance() {
    let current_balance = 5;
    let amount = 2;
    let new_balance = update_account_balance(current_balance, amount);
    assert!(balance_update_is_correct(current_balance, amount, new_balance));
}

#[test]
fn test_update_account_balance_random() {
    let current_balance = rand::random();
    let amount = rand::random();
    let result = update_account_balance(current_balance, amount);
    assert!(balance_update_is_correct(current_balance, amount, result));
}

#[test]
#[cfg_attr(kani, kani::proof)]
fn test_update_account_balance_bolero() {
    bolero::check!().with_type::<(i32, i32)>().cloned().for_each(|(current_balance, amount)| {
        let result = update_account_balance(current_balance, amount);
        assert!(balance_update_is_correct(current_balance, amount, result));
    });
}

#[cfg(kani)]
#[kani::proof]
fn test_update_account_balance_kani() {
    let current_balance = kani::any();
    let amount = kani::any();
    let result = update_account_balance(current_balance, amount);
    assert!(balance_update_is_correct(current_balance, amount, result));
}
