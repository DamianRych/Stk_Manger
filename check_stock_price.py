import requests
import random
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from typing import Dict


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
    print("HTML content:", response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the `div` with `data-attrid="Price"`
    price_div = soup.find("div", {"data-attrid": "Price"})
    
    # Find the `span` containing text that includes "EUR" and retrieve its previous sibling (the stock price)
    if price_div:
        eur_span = price_div.find("span", string=lambda text: text and "EUR" in text)
        if eur_span and eur_span.previous_sibling:
            # Convert the price text to a float
            price_text = eur_span.previous_sibling.text
            price = float(price_text.replace(",", "."))
            return price
    return None  # Return None if the price is not found

def check_stock_price(stock_symbol: str) -> Dict[str, object]:
    # while True:
    try:
        # Get the current stock price
        price = get_stock_price_google(stock_symbol)
        if price is not None:
            return {
                "price": price,
                "timestamp": datetime.now(timezone.utc).isoformat(),  # Use UTC timestamp in ISO format,
                "stock": stock_symbol
            }
        else:
            raise ValueError(f"Failed to retrieve stock price for symbol: {stock_symbol}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching stock price for {stock_symbol}")

# Set stock symbol, target price in EUR
stock_symbol = "Diageo"
# target_price = 28.90  # Set your target price here

print(check_stock_price(stock_symbol))
