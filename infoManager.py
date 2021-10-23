import torch


class InfoManager(object):
    white = []
    black = []
    team_list = []
    white_info = []
    black_info = []
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
        InfoManager.white_info.clear()
        InfoManager.black_info.clear()
        InfoManager.cur_unit.clear()

        for i in InfoManager.white:
            if i.skin == "a":
                InfoManager.cur_unit.append(1)
            elif i.skin == "d":
                InfoManager.cur_unit.append(2)
            elif i.skin == "g":
                InfoManager.cur_unit.append(3)
            InfoManager.cur_unit.append(i.posX)
            InfoManager.cur_unit.append(i.posY)
            InfoManager.white_info.append(InfoManager.cur_unit)

        for i in InfoManager.black:
            if i.skin == "a":
                InfoManager.cur_unit.append(1)
            elif i.skin == "d":
                InfoManager.cur_unit.append(2)
            elif i.skin == "g":
                InfoManager.cur_unit.append(3)
            InfoManager.cur_unit.append(i.posX)
            InfoManager.cur_unit.append(i.posY)
            InfoManager.black_info.append(InfoManager.cur_unit)

    @staticmethod
    def get_torch():
        return torch.IntTensor(InfoManager.white_info, InfoManager.black_info)

    @staticmethod
    def create(white, black):
        InfoManager.team_config("white", white)
        InfoManager.team_config("black", black)
        InfoManager.update_team_list()
        InfoManager.info_update()
        return InfoManager.get_torch()