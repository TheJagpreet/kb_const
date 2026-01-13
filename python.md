# Python Domain Knowledge

## Overview
Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for web development, data science, automation, and AI/ML applications.

## Key Concepts
- **Dynamic Typing**: Variables don't require explicit type declarations.
- **Indentation**: Uses whitespace for code blocks instead of braces.
- **Standard Library**: Extensive built-in modules for various tasks.
- **Virtual Environments**: Isolated environments for project dependencies using venv or conda.
- **Popular Frameworks**: Django/Flask for web, Pandas/NumPy for data, TensorFlow/PyTorch for ML.

## Best Practices
- Follow PEP 8 style guidelines for consistent code.
- Use list comprehensions and generators for efficient data processing.
- Implement proper exception handling with try/except blocks.
- Write docstrings for functions and classes.
- Use type hints (introduced in Python 3.5+) for better code clarity.

## Example
```python
def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

# List comprehension
squares = [x**2 for x in range(10)]

# Exception handling
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```