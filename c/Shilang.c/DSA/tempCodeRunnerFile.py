def factorial_recursive(n):
   
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")

    
    if n == 0:
        return 1
   
    else:
        return n * factorial_recursive(n - 1)

number = 5
factorial_of_5 = factorial_recursive(number)

print("Shivansh\n230410107124")
print(f"The factorial of {number} is: {factorial_of_5}")
