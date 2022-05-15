from fighter import Fighter
import torch

from heatmaper import Heatmaper
from neural import Neural
from statManager import StatManager
from situationRater import SituationRater
from net import Net

# In terminal:
# pip install seaborn
# pip install torch

'''test = [[1, -3], [0, -2]]
fighter = Fighter()
print("test", fighter.get_data(test))'''

acs = []
stat = []

neo1 = Neural(3, 5, "Clare", 2, 1, 0.005, 0)
neo1.change_super_parameters(1e-5, 300, 0.005, 200)
neo1.init_net()
acs.append(neo1.train())
stat = neo1.add_stat(stat)

print(acs)

StatManager.create_stat(stat)
StatManager.show_all()

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
