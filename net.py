import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
   def __init__(self):
       super(Net, self).__init__()
       self.fc1 = nn.Linear(2*2, 20)
       self.fc2 = nn.Linear(20, 20)
       self.fc3 = nn.Linear(20, 3)

def forward(self, x):
   x = F.relu(self.fc1(x))
   x = F.relu(self.fc2(x))
   x = self.fc3(x)
   return F.log_softmax(x)