import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    layers = 2
    layer_size = 20
    fc = []

    def __init__(self, size, layer_size):
        # self.layers = layers
        self.layer_size = layer_size

        super(Net, self).__init__()
        '''for i in range(layers):
            if i == 0:
                self.fc.append(nn.Linear(size, layer_size))
            self.fc.append(nn.Linear(layer_size, layer_size))
        self.fc.append(nn.Linear(layer_size, 3))'''

        self.fc1 = nn.Linear(size, layer_size)
        self.fc2 = nn.Linear(layer_size, layer_size)
        self.fc3 = nn.Linear(layer_size, layer_size)
        # self.fc4 = nn.Linear(layer_size, layer_size)
        self.fcL = nn.Linear(layer_size, 3)

    def forward(self, x):
        '''for i in range(self.layers):
            x = F.relu(self.fc[i](x))
        x = self.self.fc[len(self.fc) - 1](x)'''

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        # x = F.relu(self.fc4(x))
        x = self.fcL(x)
        return F.log_softmax(x)
