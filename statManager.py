from heatmaper import Heatmaper
import matplotlib.pyplot as plt
import asyncio


class StatManager:

    @staticmethod
    def create_stat(array):
        heatmapers = []
        unnamed = 1
        for i in range(len(array)):
            if array[i][0] == "Unnamed":
                array[i][0] += str(unnamed)
                unnamed += 1
            heatmapers.append(Heatmaper(array[i][0], array[i][1]))
            heatmapers[i].hm_acc()
            heatmapers[i].hm_diff()

    @staticmethod
    def show_all():
        print("Showing will stop process until you close the charts. Do you really want to show all statistic "
              "pictures? [y/N]")
        s = str(input())
        if s.lower() == "y" or s.lower() == "yes":
            plt.show()
        else:
            print("Showing cancelled")
