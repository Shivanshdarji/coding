from models import db
import yfinance as yf
from datetime import datetime

def update_portfolio_values(investments):
    """Update current values for all investments"""
    for investment in investments:
        try:
            stock_data = yf.Ticker(investment.stock_symbol).history(period='1d')
            if not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                investment.current_value = current_price * investment.shares
                db.session.commit()
        except Exception as e:
            print(f"Error updating {investment.stock_symbol}: {str(e)}")
    return investments

def calculate_portfolio_metrics(investments):
    """Calculate portfolio metrics and prepare chart data"""
    symbols = []
    amounts = []
    total_invested = 0
    total_current = 0
    
    for investment in investments:
        symbols.append(investment.stock_symbol)
        amounts.append(float(investment.amount_invested))
        total_invested += investment.amount_invested
        
        if hasattr(investment, 'current_value') and investment.current_value:
            total_current += investment.current_value
    
    return {
        'symbols': symbols,
        'amounts': amounts,
        'total_invested': total_invested,
        'total_current': total_current,
        'growth_percent': ((total_current - total_invested) / total_invested * 100) if total_invested > 0 else 0
    }