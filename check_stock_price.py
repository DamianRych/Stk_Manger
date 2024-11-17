import argparse
import requests
import random
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import re
from typing import TypedDict
# from forex_python.converter import CurrencyRates


# Define the exact structure of the dictionary using TypedDict
class StockPriceDict(TypedDict):
    price: float
    timestamp: str
    stock: str

def get_stock_price_google(stock_symbol):
    url = f"https://www.google.com/search?q={stock_symbol}+stock+price"
    
    # List of various User-Agent strings to mimic different browsers
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),  # Choose a random User-Agent
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"  # Mimic a Google search referrer
    }
    
    response = requests.get(url, headers=headers)
    print(f"HTTP Response Status Code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the `div` with `data-attrid="Price"`
    price_div = soup.find("div", {"data-attrid": "Price"})
    price_value = None
    currency = None
    
    # Find the `span` containing text that includes "EUR" and retrieve its previous sibling (the stock price)
    if price_div:
        # Find the first <span> that contains a number with two decimal digits
        span_with_price = price_div.find("span", string=re.compile(r"\d+[,\.]\d{2}"))
        
        if span_with_price:
            # Extract the value from span_with_price
            price_value = span_with_price.text
            price_value = price_value.replace(",", ".")
            
            # Find the next <span> after span_with_price
            next_span = span_with_price.find_next("span")
            if next_span:
                currency = next_span.text
    return price_value, currency  # Return None if the price is not found

# def convert_currency(amount: float, from_currency: str, to_currency: str = "USD") -> float:
#     currency_rates = CurrencyRates()
#     print(amount, from_currency, to_currency)
#     try:
#         # Fetch the conversion rate and calculate the converted amount
#         converted_amount = currency_rates.convert(from_currency, to_currency, amount)
#         return converted_amount
#     except Exception as e:
#         raise RuntimeError(f"Currency conversion error: {e}")


def check_stock_price(stock_symbol: str) -> StockPriceDict:
    try:
        # Get the current stock price
        price, currency = get_stock_price_google(stock_symbol)
        # if currency != "USD":
        #     convert_currency(price, currency)
        if price is not None:
            return {
                "price": float(price),
                "timestamp": datetime.now(timezone.utc).isoformat(),  # Use UTC timestamp in ISO format
                "stock": stock_symbol,
                "currency": currency,
            }
        else:
            raise ValueError(f"Failed to retrieve stock price for symbol: {stock_symbol}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching stock price for {stock_symbol}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get stock prices from Google Search.")
    parser.add_argument(
        "-stock_symbol", 
        type=str, 
        required=True, 
        help="The stock symbol to check."
    )
    args = parser.parse_args()

    stock_symbol = args.stock_symbol
    print(check_stock_price(stock_symbol))
