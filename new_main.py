from fighter import Fighter
import torch
from neural import Neural
from situationRater import SituationRater
from net import Net
'''test = [[1, -3], [0, -2]]
fighter = Fighter()
print("test", fighter.get_data(test))'''

accuracies = []

neo = Neural(3, 5, "Fernando", 2, 1)
neo.change_super_parameters(1e-4, 50, 0.5, 120)
neo.init_net()
accuracies.append(neo.train())

print(accuracies)

'''n = Net(34, 120)
n.load_state_dict(torch.load("test.ckpt"))
n.eval()
'''

'''x = [[2, 0, 1, 0, 0, 0, -2, -2, -1],
     [3, 1, 2, 0, 0, 0, -1, -3, 0],
     [0, 1, 2, 1, 0, 0, 0, -1, 0],
     [0, 0, 3, 3, 0, 0, 0, -1, 0]]
sr = SituationRater()
sr.reset()
sr.fill(x)
print(sr.left, sr.right)
print("rating")
print(sr.rate())'''
