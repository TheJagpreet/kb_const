# Rust Domain Knowledge

## Overview
Rust is a systems programming language focused on safety, speed, and concurrency. It guarantees memory safety without a garbage collector through its ownership system and borrowing rules.

## Key Concepts
- **Ownership**: Each value has a single owner, preventing data races.
- **Borrowing**: References with rules to ensure safe memory access.
- **Lifetimes**: Compiler-enforced scopes for references.
- **Cargo**: Package manager and build system for Rust.
- **Zero-Cost Abstractions**: High-level features with no runtime overhead.
- **Pattern Matching**: Powerful control flow with match expressions.

## Best Practices
- Embrace the borrow checker for safe code.
- Use Result and Option types for error handling instead of exceptions.
- Write tests with the built-in test framework.
- Use Cargo workspaces for multi-crate projects.
- Follow Rust naming conventions (snake_case for functions/variables).
- Leverage the rich ecosystem of crates on crates.io.

## Example
```rust
// Basic Rust program
fn main() {
    println!("Hello, Rust!");
    
    let numbers = vec![1, 2, 3, 4, 5];
    let sum: i32 = numbers.iter().sum();
    println!("Sum: {}", sum);
}

// Struct and implementation
struct User {
    name: String,
    age: u32,
}

impl User {
    fn new(name: String, age: u32) -> User {
        User { name, age }
    }
    
    fn greet(&self) {
        println!("Hello, my name is {} and I am {} years old.", self.name, self.age);
    }
}

fn main() {
    let user = User::new("Alice".to_string(), 30);
    user.greet();
}
```