import logging
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TradingBot:
    def __init__(self):
        """Initialize the trading bot with Binance Testnet credentials"""
        self.api_key = config.API_KEY
        self.api_secret = config.API_SECRET
        self.base_url = config.BASE_URL
        
        logger.info("✓ Trading Bot initialized successfully")
        logger.info(f"✓ Using Binance Testnet: {self.base_url}")
        
        # Test connection
        self._test_connection()
    
    def _generate_signature(self, params):
        """Generate HMAC SHA256 signature"""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _test_connection(self):
        """Test API connection"""
        try:
            url = f"{self.base_url}/api/v3/ping"
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("✓ Successfully connected to Binance Testnet")
                return True
            else:
                logger.error(f"✗ Connection failed: {response.text}")
                return False
        except Exception as e:
            logger.error(f"✗ Connection error: {e}")
            return False
    
    def _make_request(self, method, endpoint, params=None, signed=False):
        """Make API request"""
        url = f"{self.base_url}{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key}
        
        if params is None:
            params = {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, params=params)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None

    def get_account_balance(self):
        """Get account balance"""
        try:
            logger.info("\n=== Fetching Account Balance ===")
            data = self._make_request('GET', '/api/v3/account', signed=True)
            
            if data and 'balances' in data:
                logger.info("\n=== Account Balances ===")
                for balance in data['balances']:
                    free = float(balance['free'])
                    locked = float(balance['locked'])
                    if free > 0 or locked > 0:
                        logger.info(f"{balance['asset']}: Free={free}, Locked={locked}")
                return data['balances']
            else:
                logger.error("Failed to get balance")
                return None
                
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return None

    def get_current_price(self, symbol):
        """Get current market price for a symbol"""
        try:
            data = self._make_request('GET', '/api/v3/ticker/price', {'symbol': symbol})
            
            if data and 'price' in data:
                price = float(data['price'])
                logger.info(f"Current {symbol} price: ${price:,.2f}")
                return price
            else:
                logger.error(f"Failed to get price for {symbol}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting price: {e}")
            return None

    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Amount to trade
        """
        try:
            logger.info(f"\n=== Placing {side} Market Order ===")
            logger.info(f"Symbol: {symbol}")
            logger.info(f"Quantity: {quantity}")
            
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity
            }
            
            data = self._make_request('POST', '/api/v3/order', params, signed=True)
            
            if data:
                logger.info(f"✓ Order placed successfully!")
                logger.info(f"Order ID: {data.get('orderId')}")
                logger.info(f"Status: {data.get('status')}")
                logger.info(f"Executed Qty: {data.get('executedQty')}")
                return data
            else:
                logger.error("Failed to place order")
                return None
                
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Amount to trade
            price (float): Limit price
        """
        try:
            logger.info(f"\n=== Placing {side} Limit Order ===")
            logger.info(f"Symbol: {symbol}")
            logger.info(f"Quantity: {quantity}")
            logger.info(f"Price: ${price:,.2f}")
            
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'timeInForce': 'GTC',
                'quantity': quantity,
                'price': price
            }
            
            data = self._make_request('POST', '/api/v3/order', params, signed=True)
            
            if data:
                logger.info(f"✓ Limit order placed successfully!")
                logger.info(f"Order ID: {data.get('orderId')}")
                logger.info(f"Status: {data.get('status')}")
                return data
            else:
                logger.error("Failed to place limit order")
                return None
                
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            return None

    def get_open_orders(self, symbol):
        """Get all open orders for a symbol"""
        try:
            params = {'symbol': symbol}
            data = self._make_request('GET', '/api/v3/openOrders', params, signed=True)
            
            if data is not None:
                if len(data) > 0:
                    logger.info(f"\n=== Open Orders for {symbol} ===")
                    for order in data:
                        logger.info(f"Order ID: {order['orderId']}")
                        logger.info(f"Side: {order['side']}, Type: {order['type']}")
                        logger.info(f"Price: {order['price']}, Qty: {order['origQty']}")
                        logger.info("---")
                else:
                    logger.info(f"No open orders for {symbol}")
                return data
            else:
                logger.error("Failed to get open orders")
                return None
                
        except Exception as e:
            logger.error(f"Error getting open orders: {e}")
            return None

    def cancel_order(self, symbol, order_id):
        """Cancel an order"""
        try:
            params = {
                'symbol': symbol,
                'orderId': order_id
            }
            
            data = self._make_request('DELETE', '/api/v3/order', params, signed=True)
            
            if data:
                logger.info(f"✓ Order {order_id} cancelled successfully")
                return data
            else:
                logger.error(f"Failed to cancel order {order_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return None


if __name__ == "__main__":
    # Test the bot
    bot = TradingBot()
    bot.get_account_balance()
    bot.get_current_price(config.DEFAULT_SYMBOL)