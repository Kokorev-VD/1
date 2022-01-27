import torch
import numpy as np


class InfoManager(object):
    white = []
    black = []
    team_list = []
    teams_info = []
    cur_unit = []

    @staticmethod
    def team_config(color, team):
        if color == "white":
            InfoManager.white = team
        if color == "black":
            InfoManager.black = team

    @staticmethod
    def update_team_list():
        InfoManager.team_list.clear()
        InfoManager.team_list.append(InfoManager.white)
        InfoManager.team_list.append(InfoManager.black)

    @staticmethod
    def info_update():
        InfoManager.teams_info.clear()
        InfoManager.cur_unit.clear()

        counter = 0

        for i in InfoManager.white:
            counter += 1
            InfoManager.cur_unit = []
            print("unit ", counter, " initialisation")
            print("unit team - white")
            InfoManager.cur_unit.append(1)
            if i.skin == "a":
                InfoManager.cur_unit.append(1)
            elif i.skin == "d":
                InfoManager.cur_unit.append(2)
            elif i.skin == "g":
                InfoManager.cur_unit.append(3)
            print("type of unit - ", InfoManager.cur_unit[0])
            InfoManager.cur_unit.append(i.x_position)
            print("x of unit - ", InfoManager.cur_unit[1])
            InfoManager.cur_unit.append(i.y_position)
            print("y of unit - ", InfoManager.cur_unit[2])
            print(InfoManager.cur_unit)
            InfoManager.teams_info.append(InfoManager.cur_unit)

        for i in InfoManager.black:
            counter += 1
            InfoManager.cur_unit = []
            print("unit ", counter, " initialisation")
            print("unit team - black")
            InfoManager.cur_unit.append(2)
            if i.skin == "a":
                InfoManager.cur_unit.append(1)
            elif i.skin == "d":
                InfoManager.cur_unit.append(2)
            elif i.skin == "g":
                InfoManager.cur_unit.append(3)
            print("type of unit - ", InfoManager.cur_unit[0])
            InfoManager.cur_unit.append(i.x_position)
            print("x of unit - ", InfoManager.cur_unit[1])
            InfoManager.cur_unit.append(i.y_position)
            print("y of unit - ", InfoManager.cur_unit[2])
            print(InfoManager.cur_unit)
            InfoManager.teams_info.append(InfoManager.cur_unit)

    @staticmethod
    def get_torch():
        return torch.IntTensor(InfoManager.teams_info)

    @staticmethod
    def create(white, black):
        InfoManager.team_config("white", white)
        InfoManager.team_config("black", black)
        InfoManager.update_team_list()
        InfoManager.info_update()
        return InfoManager.get_torch()
