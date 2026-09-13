from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Investment
#from stock_predictor_pt import StockPredictor
from stock_predictor import StockPredictor  # Using PyTorch version
import yfinance as yf
from datetime import datetime, timedelta
import os
import warnings
from datetime import datetime, timedelta
import yfinance as yf
from models import db, User, Investment
from flask import Flask
from models import db
from portfolio.routes import portfolio_bp
from stock_predictor_pt import StockPredictor
from flask import Flask
from models import db
from portfolio.routes import portfolio_bp
from auth.routes import auth_bp  # This will resolve the yellow line

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Configure database (add this right after creating Flask app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize extensions
db.init_app(app)

@app.route('/')
def home():
    return "Welcome to Stock Predictor!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login Page"

@app.route('/register')
def register():
    return "Registration Page"

# Register blueprints
app.register_blueprint(portfolio_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')  # All auth routes will be under /auth

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(portfolio_bp)

# Import other routes
from auth import auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# Suppress warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
        else:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    investments = Investment.query.filter_by(user_id=user.id).all()
    
    # Update current values
    total_invested = 0
    total_current = 0
    for investment in investments:
        try:
            stock_data = yf.Ticker(investment.stock_symbol).history(period='1d')
            if not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                investment.current_value = current_price * investment.shares
                total_invested += investment.amount_invested
                total_current += investment.current_value
        except:
            investment.current_value = None
    
    return render_template('dashboard.html', 
                         user=user, 
                         investments=investments,
                         total_invested=total_invested,
                         total_current=total_current)

@app.route('/invest', methods=['GET', 'POST'])
def invest():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        amount = float(request.form['amount'])
        
        if amount < 100:
            flash('Minimum investment is ₹100', 'danger')
            return redirect(url_for('invest'))
        
        try:
            # Get stock data
            stock = yf.Ticker(symbol)
            hist = stock.history(period='1d')
            
            if hist.empty:
                flash('Invalid stock symbol or no data available', 'danger')
                return redirect(url_for('invest'))
            
            current_price = hist['Close'].iloc[-1]
            shares = amount / current_price
            
            # Make prediction (with error handling)
            try:
                predictor = StockPredictor(symbol)
                prediction = predictor.predict_future()
                predicted_growth = prediction['predicted_growth']
            except Exception as e:
                print(f"Prediction error: {e}")
                predicted_growth = 0  # Default value if prediction fails
            
            # Record investment
            new_investment = Investment(
                user_id=session['user_id'],
                stock_symbol=symbol,
                amount_invested=amount,
                shares=shares,
                buy_price=current_price,
                buy_date=datetime.now(),
                predicted_growth=predicted_growth
            )
            
            db.session.add(new_investment)
            db.session.commit()
            
            flash(f'Successfully invested ₹{amount:.2f} in {symbol}', 'success')
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            print(f"Investment error: {e}")
            flash('Error processing your investment. Please try again.', 'danger')
    
    return render_template('invest.html')

@app.route('/portfolio')
def portfolio():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    investments = Investment.query.filter_by(user_id=user.id).all()
    
    # Prepare data for chart
    symbols = [inv.stock_symbol for inv in investments]
    amounts = [inv.amount_invested for inv in investments]
    
    return render_template('portfolio.html',
                         user=user,
                         investments=investments,
                         symbols=symbols,
                         amounts=amounts)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)