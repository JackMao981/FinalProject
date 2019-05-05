def factorial(n):
    """ Computes the factorial of the non-negative integer n """
    return_val = 1
    breakpoint()
    for i in range(n):
        return_val *= i
    return return_val

if __name__ == '__main__':
    print(factorial(5))
