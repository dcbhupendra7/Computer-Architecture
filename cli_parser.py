import sys

def parse_params(args):
    if len(args) != 3:
        print_usage()
        raise ValueError("Incorrect number of arguments")

    params = {}
    for arg in args:
        if len(arg) < 2:
            raise ValueError(f"Invalid argument format: {arg}")
        option = arg[1]
        value_str = arg[2:]
        try:
            value = int(value_str)
        except ValueError:
            raise ValueError(f"Invalid value for argument {option}: {value_str}")
        params[option] = value

    if 'c' not in params or 'b' not in params or 'a' not in params:
        raise ValueError("Missing required parameters")

    return params['c'], params['b'], params['a']

def print_usage():
    print("Usage: python main.py -c<capacity> -b<blocksize> -a<associativity>")
    print("  <capacity> in KB: 4, 8, 16, 32, or 64")
    print("  <blocksize> in bytes: 4, 8, 16, 32, 64, 128, 256, or 512")
    print("  <associativity>: 1, 2, 4, 8, 16")
