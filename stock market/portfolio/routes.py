from flask import Blueprint, render_template, session, redirect, url_for
from models import User, Investment
import yfinance as yf
from datetime import datetime
from .utils import update_portfolio_values, calculate_portfolio_metrics

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio_bp.route('/')
def portfolio():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    investments = Investment.query.filter_by(user_id=user.id).all()
    
    # Update and calculate portfolio data
    investments = update_portfolio_values(investments)
    metrics = calculate_portfolio_metrics(investments)
    
    return render_template('portfolio.html',
                         user=user,
                         investments=investments,
                         **metrics)

@portfolio_bp.route('/<symbol>')
def stock_detail(symbol):
    # Add individual stock detail view if needed
    pass