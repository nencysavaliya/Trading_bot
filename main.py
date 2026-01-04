import sys
from bot import TradingBot
import config
import logging

logger = logging.getLogger(__name__)


def print_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("🤖 BINANCE TRADING BOT - TESTNET")
    print("="*50)
    print("1. Check Account Balance")
    print("2. Get Current Price")
    print("3. Place Market Order (Buy)")
    print("4. Place Market Order (Sell)")
    print("5. Place Limit Order (Buy)")
    print("6. Place Limit Order (Sell)")
    print("7. View Open Orders")
    print("8. Cancel Order")
    print("9. Exit")
    print("="*50)


def get_valid_input(prompt, input_type=str):
    """Get and validate user input"""
    while True:
        try:
            user_input = input(prompt)
            if input_type == float:
                return float(user_input)
            elif input_type == int:
                return int(user_input)
            else:
                return user_input
        except ValueError:
            print(f"❌ Invalid input. Please enter a valid {input_type.__name__}")


def main():
    """Main function to run the trading bot CLI"""
    print("\n🚀 Initializing Trading Bot...")
    
    try:
        bot = TradingBot()
    except Exception as e:
        print(f"❌ Failed to initialize bot: {e}")
        return
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-9): ")
        
        if choice == '1':
            # Check Account Balance
            print("\n📊 Fetching account balance...")
            bot.get_account_balance()
        
        elif choice == '2':
            # Get Current Price
            symbol = input(f"\nEnter symbol (default: {config.DEFAULT_SYMBOL}): ").upper()
            if not symbol:
                symbol = config.DEFAULT_SYMBOL
            bot.get_current_price(symbol)
        
        elif choice == '3':
            # Place Market Buy Order
            print("\n💰 PLACE MARKET BUY ORDER")
            symbol = input(f"Enter symbol (default: {config.DEFAULT_SYMBOL}): ").upper()
            if not symbol:
                symbol = config.DEFAULT_SYMBOL
            
            quantity = get_valid_input(
                f"Enter quantity (default: {config.DEFAULT_QUANTITY}): ",
                float
            ) or config.DEFAULT_QUANTITY
            
            confirm = input(f"\n⚠️ Confirm BUY {quantity} {symbol} at MARKET price? (yes/no): ")
            if confirm.lower() == 'yes':
                bot.place_market_order(symbol, 'BUY', quantity)
            else:
                print("❌ Order cancelled")
        
        elif choice == '4':
            # Place Market Sell Order
            print("\n💸 PLACE MARKET SELL ORDER")
            symbol = input(f"Enter symbol (default: {config.DEFAULT_SYMBOL}): ").upper()
            if not symbol:
                symbol = config.DEFAULT_SYMBOL
            
            quantity = get_valid_input(
                f"Enter quantity (default: {config.DEFAULT_QUANTITY}): ",
                float
            ) or config.DEFAULT_QUANTITY
            
            confirm = input(f"\n⚠️ Confirm SELL {quantity} {symbol} at MARKET price? (yes/no): ")
            if confirm.lower() == 'yes':
                bot.place_market_order(symbol, 'SELL', quantity)
            else:
                print("❌ Order cancelled")
        
        elif choice == '5':
            # Place Limit Buy Order
            print("\n💰 PLACE LIMIT BUY ORDER")
            symbol = input(f"Enter symbol (default: {config.DEFAULT_SYMBOL}): ").upper()
            if not symbol:
                symbol = config.DEFAULT_SYMBOL
            
            # Show current price first
            current_price = bot.get_current_price(symbol)
            
            quantity = get_valid_input(
                f"Enter quantity (default: {config.DEFAULT_QUANTITY}): ",
                float
            ) or config.DEFAULT_QUANTITY
            
            price = get_valid_input("Enter limit price: ", float)
            
            confirm = input(f"\n⚠️ Confirm BUY {quantity} {symbol} at ${price}? (yes/no): ")
            if confirm.lower() == 'yes':
                bot.place_limit_order(symbol, 'BUY', quantity, price)
            else:
                print("❌ Order cancelled")
        
        elif choice == '6':
            # Place Limit Sell Order
            print("\n💸 PLACE LIMIT SELL ORDER")
            symbol = input(f"Enter symbol (default: {config.DEFAULT_SYMBOL}): ").upper()
            if not symbol:
                symbol = config.DEFAULT_SYMBOL
            
            # Show current price first
            current_price = bot.get_current_price(symbol)
            
            quantity = get_valid_input(
                f"Enter quantity (default: {config.DEFAULT_QUANTITY}): ",
                float
            ) or config.DEFAULT_QUANTITY
            
            price = get_valid_input("Enter limit price: ", float)
            
            confirm = input(f"\n⚠️ Confirm SELL {quantity} {symbol} at ${price}? (yes/no): ")
            if confirm.lower() == 'yes':
                bot.place_limit_order(symbol, 'SELL', quantity, price)
            else:
                print("❌ Order cancelled")
        
        elif choice == '7':
            # View Open Orders
            symbol = input(f"\nEnter symbol (default: {config.DEFAULT_SYMBOL}): ").upper()
            if not symbol:
                symbol = config.DEFAULT_SYMBOL
            bot.get_open_orders(symbol)
        
        elif choice == '8':
            # Cancel Order
            symbol = input(f"\nEnter symbol (default: {config.DEFAULT_SYMBOL}): ").upper()
            if not symbol:
                symbol = config.DEFAULT_SYMBOL
            
            order_id = get_valid_input("Enter Order ID to cancel: ", int)
            
            confirm = input(f"\n⚠️ Confirm cancel order {order_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                bot.cancel_order(symbol, order_id)
            else:
                print("❌ Cancellation aborted")
        
        elif choice == '9':
            # Exit
            print("\n👋 Exiting Trading Bot. Goodbye!")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-9")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)