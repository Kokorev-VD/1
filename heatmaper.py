import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# named_tuple = time.localtime()  # получить struct_time
# time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)


class Heatmaper:
    def __init__(self, name, accuracies):
        self.name = name
        self.accuracies = accuracies

    def hm_acc(self):
        named_tuple = time.localtime()
        time_string = time.strftime("%d-%m", named_tuple)
        self.filename = self.name.lower() + "-accuracies-" + time_string + ".png"

        array = []
        for i in range(len(self.accuracies)):
            array.append(round(self.accuracies[i], 2))

        data = np.array([array])
        plt.figure(figsize=(10, 6))
        heatmap = sns.heatmap(data, vmin=min(array), vmax=max(array), annot=True, yticklabels=False, cmap="cool",
                              cbar_kws={'label': 'Color range', 'orientation': 'horizontal'},
                              annot_kws={'rotation': 90},
                              linewidths=1)
        heatmap.set_title("Accuracies of  " + self.name, fontdict={'fontsize': 12}, pad=12)
        # plt.xticks(rotation=35)
        plt.ylabel("Accuracies")
        plt.xlabel('Epoch number')
        plt.savefig(self.filename, dpi=100, bbox_inches='tight')

    def hm_diff(self):
        named_tuple = time.localtime()
        time_string = time.strftime("%d-%m", named_tuple)
        self.filename = self.name.lower() + "-difference-" + time_string + ".png"

        array = [0]
        for i in range(1, len(self.accuracies)):
            array.append(round(self.accuracies[i] - self.accuracies[i - 1], 2))

        minimum = 100
        for i in range(1, len(array)):
            if array[i] < minimum:
                minimum = array[i]

        data = np.array([array])
        plt.figure(figsize=(10, 6))
        h_m = sns.heatmap(data, vmin=minimum, vmax=max(array), annot=True, yticklabels=False, cmap="cool",
                          cbar_kws={'label': 'Color range', 'orientation': 'horizontal'}, annot_kws={'rotation': 90},
                          linewidths=1)
        h_m.set_title("Accuracy difference of  " + self.name, fontdict={'fontsize': 12}, pad=12)
        # plt.xticks(rotation=35)
        plt.ylabel("Accuracy difference")
        plt.xlabel('Epoch number')
        plt.savefig(self.filename, dpi=100, bbox_inches='tight')
