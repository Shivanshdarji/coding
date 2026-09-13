import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    investments = db.relationship('Investment', backref='investor', lazy=True)

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    amount_invested = db.Column(db.Float, nullable=False)
    shares = db.Column(db.Float, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    buy_date = db.Column(db.DateTime, nullable=False)
    predicted_growth = db.Column(db.Float)
    current_value = db.Column(db.Float)
    sold = db.Column(db.Boolean, default=False)
    sell_price = db.Column(db.Float)
    sell_date = db.Column(db.DateTime)

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class StockDataset(Dataset):
    def __init__(self, data, sequence_length=60):
        self.data = data
        self.seq_length = sequence_length
        
    def __len__(self):
        return len(self.data) - self.seq_length
    
    def __getitem__(self, idx):
        x = self.data[idx:idx+self.seq_length]
        y = self.data[idx+self.seq_length]
        return torch.FloatTensor(x).view(-1, 1), torch.FloatTensor([y])

class LSTM_Model(nn.Module):
    def __init__(self, input_size=1, hidden_size=50, num_layers=3):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.dropout = nn.Dropout(0.2)
        self.fc = nn.Linear(hidden_size, 1)
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.dropout(out[:, -1, :])
        out = self.fc(out)
        return out

class StockPredictor:
    def __init__(self, symbol):
        self.symbol = symbol
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = LSTM_Model().to(device)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.sequence_length = 60
    
    def _get_data(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*2)  # 2 years data
        data = yf.download(self.symbol, start=start_date, end=end_date)
        return data['Close'].values.reshape(-1, 1)
    
    def _prepare_data(self, data):
        scaled_data = self.scaler.fit_transform(data)
        dataset = StockDataset(scaled_data, self.sequence_length)
        
        # Split into train and test
        train_size = int(0.8 * len(dataset))
        test_size = len(dataset) - train_size
        train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])
        
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        
        return train_loader, test_loader
    
    def train(self, epochs=50):
        data = self._get_data()
        train_loader, test_loader = self._prepare_data(data)
        
        self.model.train()
        for epoch in range(epochs):
            for batch_x, batch_y in train_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                
                self.optimizer.zero_grad()
                outputs = self.model(batch_x)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()
            
            # Validation
            self.model.eval()
            val_loss = 0
            with torch.no_grad():
                for batch_x, batch_y in test_loader:
                    batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                    outputs = self.model(batch_x)
                    val_loss += self.criterion(outputs, batch_y).item()
            
            val_loss /= len(test_loader)
            print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}')
            self.model.train()
    
    def predict_future(self, days=7):
        self.train(epochs=30)  # Train with fewer epochs for faster prediction
        
        data = self._get_data()
        scaled_data = self.scaler.transform(data)
        
        self.model.eval()
        predictions = []
        last_sequence = scaled_data[-self.sequence_length:]
        
        with torch.no_grad():
            for _ in range(days):
                x = torch.FloatTensor(last_sequence).view(1, -1, 1).to(device)
                pred = self.model(x).cpu().numpy()[0][0]
                predictions.append(pred)
                last_sequence = np.append(last_sequence[1:], pred)
        
        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        
        current_price = data[-1][0]
        predicted_prices = [p[0] for p in predictions]
        predicted_growth = ((predicted_prices[-1] - current_price) / current_price) * 100
        
        return {
            'current_price': current_price,
            'predicted_prices': predicted_prices,
            'predicted_growth': predicted_growth
        }