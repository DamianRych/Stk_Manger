# get_stock_symbols.py
import json
from typing import List

def get_stock_symbols() -> List[str]:
    """
    Dynamically generate or fetch stock symbols.

    Returns:
        List[str]: A list of stock symbols.
    """
    # Example valid return value
    return ["Nestle", "Diageo"]
    # Example invalid return value for testing:
    # return ["Nestle", 123]  # Uncomment to test the error

def validate_stock_symbols(symbols: List[str]) -> List[str]:
    """
    Validates that the given value is a list of strings.

    Args:
        symbols (List[str]): The list of stock symbols to validate.

    Returns:
        List[str]: The validated list of stock symbols.

    Raises:
        TypeError: If the input is not a list of strings.
    """
    if not isinstance(symbols, list):
        raise TypeError(f"Expected a list, but got {type(symbols).__name__}.")
    if not all(isinstance(symbol, str) for symbol in symbols):
        raise TypeError("All elements in the list must be strings.")
    return symbols

if __name__ == "__main__":
    stock_symbols = get_stock_symbols()
    try:
        # Validate the return type of get_stock_symbols
        stock_symbols = validate_stock_symbols(stock_symbols)
        # Output each symbol on a new line
        for symbol in stock_symbols:
            print(symbol)
    except TypeError as e:
        print(f"Error: {e}")
