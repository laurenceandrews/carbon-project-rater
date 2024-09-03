import torch
import torch.nn as nn
import torch.optim as optim

class SimpleNN(nn.Module):
    def __init__(self, input_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def train_pytorch_model(data):
    X = torch.tensor(data.drop('total_mass_co2_sequestered', axis=1).values, dtype=torch.float32)
    y = torch.tensor(data['total_mass_co2_sequestered'].values, dtype=torch.float32).view(-1, 1)
    
    model = SimpleNN(X.shape[1])
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(100):
        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
    
    torch.save(model.state_dict(), '/app/ml_models/pytorch_model.pth')
    return loss.item()

def predict_with_pytorch_model(input_data):
    model = SimpleNN(input_data.shape[1])
    model.load_state_dict(torch.load('/app/ml_models/pytorch_model.pth'))
    return model(input_data)
