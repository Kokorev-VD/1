import torch
from torch.utils.data import TensorDataset, random_split, DataLoader
from net import Net
import numpy as np
from fighter import Fighter
import torch.nn as nn
import torch.optim as optim
from situationRater import SituationRater
# from pytorch_lightning import Trainer
import time
from fieldManager import FieldManager
# from torch import Trainer


class Neural:
    # field = []
    device = 'cpu'
    size = 0
    in_data = []
    out_data = []
    in_rate = []
    length = 0
    heigth = 0
    total = 0
    learn_size = 0.8
    layer_size = 20
    rater = SituationRater()
    accuracies = []
    acc_diff = []
    timer = 0
    start = 0
    name = ""
    load_mode = 0
    train_mode = 0
    auto_stop = False
    auto_break = 0
    auto_flag = False
    in_special = []
    rate_special = []
    out_special = []
    is_gaming_neural = False

    def change_super_parameters(self, lr, n_epochs, learn_size, layer_size):
        self.lr = lr
        self.n_epochs = n_epochs
        self.learn_size = learn_size
        self.layer_size = layer_size

    def mark_as_gaming(self):
        self.is_gaming_neural = True

    def __init__(self, height, length, name, load_mode, train_mode, auto_stop, gaming_mode):
        # resetting
        self.train_mode = train_mode
        self.name = name
        self.load_mode = load_mode
        self.size = 0
        self.in_data = []
        self.in_special = []
        self.rate_special = []
        self.out_special = []
        self.out_data = []
        self.in_rate = []
        self.length = 0
        self.heigth = 0
        self.total = 0
        self.learn_size = 0.8
        self.layer_size = 20
        self.rater = SituationRater()
        self.timer = 0
        self.start = 0

        if gaming_mode == 1:
            self.mark_as_gaming()

        if auto_stop != 0:
            self.auto_stop = True
            self.auto_break = auto_stop
        else:
            self.auto_stop = False

        if len(self.name) != 0:
            print("The name of this net is ", self.name, ". It starts initialisation. ", time.asctime(), sep="")
        else:
            print("Net init starts.", time.asctime())
        self.start = time.time()
        # self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # self.field = field
        self.size = height * length
        self.heigth = height
        self.length = length
        # self.create_data([])
        if not self.is_gaming_neural:
            if load_mode == 1 or load_mode == 2:
                sin = str(height) + '_' + str(length) + '_in_rate'
                sout = str(height) + '_' + str(length) + '_out_data'
            if load_mode == 0 or load_mode == 1:
                self.timer = time.time()
                self.create_data_small([])
                print("data created in ", round((time.time() - self.timer) / 60, 3), "minutes")
                self.timer = time.time()
                self.create_answers()
                print("answers created in ", round((time.time() - self.timer) / 60, 3), "minutes")
                # self.in_np = np.array(self.in_data)
                # print(len(self.in_rate), len(self.out_data))
                self.in_np = np.array(self.in_rate)
                self.out_np = np.array(self.out_data)
                if load_mode == 1:
                    np.save(sin, self.in_np)
                    np.save(sout, self.out_np)
            if load_mode == 2:
                sin += '.npy'
                sout += '.npy'
                self.in_np = np.load(sin)
                self.out_np = np.load(sout)
                self.total = len(self.in_np)
                print("loaded", len(self.in_np), len(self.in_np))

        # Sets hyper-parameters
        self.lr = 1e-3
        self.n_epochs = 50
        self.learn_size = 0.8
        self.layers = 2
        self.layer_size = 20

    def init_net(self):
        self.timer = time.time()
        # self.model = Net(self.size, self.layer_size)
        self.model = Net(34, self.layer_size)
        torch.manual_seed(42)
        if not self.is_gaming_neural:
            self.x_tensor = torch.from_numpy(self.in_np).float()
            self.y_tensor = torch.from_numpy(self.out_np).long()

            # self.total = 7 ** (length*height)
            self.total = len(self.in_np)
            print(self.total)

            # Builds dataset with ALL data
            self.dataset = TensorDataset(self.x_tensor, self.y_tensor)
            print("creating dataset", len(self.dataset), self.total)
            # Splits randomly into train and validation datasets
            self.train_dataset, self.val_dataset = \
                random_split(self.dataset,
                             [int(self.total * self.learn_size), self.total - int(self.total * self.learn_size)])
            # Builds a loader for each dataset to perform mini-batch gradient descent
            self.train_loader = DataLoader(dataset=self.train_dataset, batch_size=14)
            self.val_loader = DataLoader(dataset=self.val_dataset, batch_size=7)
            self.accu_loader = DataLoader(dataset=self.dataset, batch_size=7)

        # Defines loss function and optimizer
        self.loss_fn = nn.CrossEntropyLoss()

        self.optimizer = optim.SGD(self.model.parameters(), lr=self.lr)

        self.losses = []
        self.val_losses = []
        # Creates function to perform train step from model, loss and optimizer
        # train_step = make_train_step(model, loss_fn, optimizer)
        print("net inited in ", round((time.time() - self.timer) / 60, 4), "minutes")

    def get_prediction(self, model, loss_fn, optimizer, x):
        with torch.no_grad:
            yhat = model(x)
            pred = yhat.tolist().index(max(yhat.tolist()[0], yhat.tolist()[1], yhat.tolist()[2]))
            return pred

    def make_train_step(self, model, loss_fn, optimizer):
        # Builds function that performs a step in the train loop
        def train_step(x, y):
            # Sets model to TRAIN mode
            model.train()
            # Makes predictions
            yhat = model(x)
            # Computes loss
            # print(y, torch.exp(yhat))
            loss = loss_fn(yhat, y)
            # Computes gradients
            loss.backward()
            # Updates parameters and zeroes gradients
            optimizer.step()
            optimizer.zero_grad()
            # Returns the loss
            return loss.item()

        # Returns the function that will be called inside the train loop
        return train_step

    def train(self):
        self.auto_flag = False
        self.accuracies = []
        self.acc_diff = []
        # trainer = Trainer()
        # trainer.fit(self.model, self.train_loader, self.val_loader)
        # Training loop
        if self.train_mode == 0 or self.train_mode == 1:
            loss_function = nn.CrossEntropyLoss()

            optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
            train_step = self.make_train_step(self.model, loss_function, optimizer)
            for epoch in range(self.n_epochs):
                self.timer = time.time()
                # Uses loader to fetch one mini-batch for training
                for x_batch, y_batch in self.train_loader:
                    # NOW, sends the mini-batch data to the device
                    # so it matches location of the MODEL
                    # x_batch = x_batch.to(self.device)
                    # y_batch = y_batch.to(self.device)
                    # One stpe of training
                    # self.loss = trainer.train(x_batch, y_batch)
                    self.loss = train_step(x_batch, y_batch)
                    self.losses.append(self.loss)

                # After finishing training steps for all mini-batches,
                # it is time for evaluation!

                # We tell PyTorch to NOT use autograd...
                # Do you remember why?
                with torch.no_grad():
                    # Uses loader to fetch one mini-batch for validation
                    for x_val, y_val in self.val_loader:
                        # Again, sends data to same device as model
                        # x_val = x_val.to(device)
                        # y_val = y_val.to(device)

                        # What is that?!
                        # model.eval()
                        # Makes predictions
                        self.yhat = self.model(x_val)
                        # Computes validation loss
                        self.val_loss = self.loss_fn(self.yhat, y_val)
                        self.val_losses.append(self.val_loss.item())
                print("epoch", epoch + 1, "has passed in", round((time.time() - self.timer) / 60, 3), "minutes, ",
                      end="")
                with torch.no_grad():
                    accuracy = self.get_acc(False)
                    s = 0
                    for i in range(len(accuracy)):
                        s += accuracy[i]
                    self.accuracies.append(s / len(accuracy) * 100)
                    print("accuracy is ", s / len(accuracy) * 100, "%", sep="")
                    if self.auto_stop:
                        if len(self.accuracies) > 1:
                            self.acc_diff.append(self.accuracies[len(self.accuracies) - 1] -
                                                 self.accuracies[len(self.accuracies) - 2])
                            if self.accuracies[len(self.accuracies) - 1] - self.accuracies[len(self.accuracies) - 2] < \
                                    self.auto_break:
                                if self.auto_flag:
                                    print(time.asctime(), "Training stopped automatically")
                                    break
                                else:
                                    print("Accuracy alert!")
                                    self.auto_flag = True
                            else:
                                self.auto_flag = False

            # print(model.state_dict())
            print(np.mean(self.losses))
            print(np.mean(self.val_losses))
        if self.train_mode == 2:
            if self.name == "":
                self.model.load_state_dict(torch.load("default.ckpt"))
            else:
                save_name = self.name + ".ckpt"
                self.model.load_state_dict(torch.load(save_name))
            self.model.eval()
        accuracy = []

        '''with torch.no_grad():
            t = 0
            for x_accu, y_accu in self.accu_loader:
                batch = torch.exp(self.model(x_accu)).tolist()
                predictions = []
                real = y_accu.tolist()
                for i in range(len(batch)):
                    t += 1
                    predictions.append(batch[i].index(max(batch[i][0], batch[i][1], batch[i][2])))
                    """m = 0
                    p = -1
                    for j in range(len(batch[i])):
                        print(int(batch[i][j] * 100))
                        if m < batch[i][j]:
                            p = j
                    predictions.append(p)"""
                    if predictions[i] == real[i]:
                        accuracy.append(1)
                    else:
                        accuracy.append(0)
                    if t % 50000 == 0:
                        print(t, batch[i], predictions[i], real[i])

                """t += 1
                self.yhat = self.model(x_accu)
                list = torch.exp(self.yhat).tolist()
                for i in range(len(list)):
                    predict = list[i].index(max(list[i][0], list[i][1], list[i][2]))
                    if predict == y_accu.tolist()[i]:
                        accuracy.append(1)
                    else:
                        accuracy.append(0)
                    print(t, x_accu.tolist()[i], predict, y_accu.tolist()[i])"""
            s = 0
            for i in range(len(accuracy)):
                s+=accuracy[i]
            print("accuracy is ", s/len(accuracy)*100, "%", sep="")
            print("accuracy got in", round((time.time() - self.timer) / 60, 2), "minutes")
            print("done in", round((time.time() - self.start) / 60, 1), "minutes")
            print(time.asctime())
            if self.train_mode == 1:
                if self.name == "":
                    torch.save(self.model.state_dict(), "default.ckpt")
                else:
                    save_name = self.name + ".ckpt"
                    torch.save(self.model.state_dict(), save_name)
            if len(self.name) != 0:
                print(self.name, "trained.", "\n")
            return s/len(accuracy)*100'''

        if not self.is_gaming_neural:
            print("getting accuracy")
            self.timer = time.time()
            accuracy = self.get_acc(True)
            s = 0
            for i in range(len(accuracy)):
                s += accuracy[i]
            print("accuracy is ", s / len(accuracy) * 100, "%", sep="")
            print("accuracy got in", round((time.time() - self.timer) / 60, 2), "minutes")
            print("done in", round((time.time() - self.start) / 60, 1), "minutes")
            print(time.asctime())
            if self.train_mode == 1:
                if self.name == "":
                    torch.save(self.model.state_dict(), "default.ckpt")
                else:
                    save_name = self.name + ".ckpt"
                    torch.save(self.model.state_dict(), save_name)
            if len(self.name) != 0:
                print(self.name, "trained.", "\n")

            return s / len(accuracy) * 100

        else:
            return "accuracy solving aborted"

    def get_best(self):
        # fighter = Fighter()
        # print("answers creating")
        for i in range(len(self.in_special)):
            # pole = self.convert_field(self.in_special[i])
            # # print(self.in_data[i], " > ", pole)
            # self.out_special.append(fighter.get_data(pole))
            # if i % 50000 == 0:
            #     print(i, self.out_data[len(self.out_special) - 1])
            self.out_special.append(404)
        # print("answers created")

        # print(len(self.out_special), len(self.in_special), len(self.rate_special))

        self.in_special_np = np.array(self.rate_special)
        self.out_special_np = np.array(self.out_special)

        # print(len(self.in_special_np), len(self.out_special_np))

        self.special_x_tensor = torch.from_numpy(self.in_special_np).float()
        self.special_y_tensor = torch.from_numpy(self.out_special_np).long()

        self.special_dataset = TensorDataset(self.special_x_tensor, self.special_y_tensor)
        self.special_loader = DataLoader(dataset=self.special_dataset, batch_size=7)

        max_pred = 0
        max_batch = []
        i_max = 0
        t = 0

        with torch.no_grad():
            for x_sp, y_sp in self.special_dataset:
                batch = torch.exp(self.model(x_sp)).tolist()
                # print(batch, end='')
                if (batch[2] > max_pred and t < len(self.in_special) - 1) or t == 0:
                    max_pred = batch[2]
                    max_batch = batch
                    i_max = t
                    # print(" <-", end='')
                # print("")
                t += 1

        answer = [max_pred, max_batch, self.in_special[i_max], i_max]
        FieldManager.set_best(answer[2])
        return answer

    def get_acc(self, flag):
        accuracy = []
        # print("getting accuracy")
        # self.timer = time.time()
        with torch.no_grad():
            t = 0
            for x_accu, y_accu in self.accu_loader:
                batch = torch.exp(self.model(x_accu)).tolist()
                predictions = []
                real = y_accu.tolist()
                for i in range(len(batch)):
                    t += 1
                    predictions.append(batch[i].index(max(batch[i][0], batch[i][1], batch[i][2])))
                    if predictions[i] == real[i]:
                        accuracy.append(1)
                    else:
                        accuracy.append(0)
                    if t % 50000 == 0 and flag:
                        print(t, batch[i], predictions[i], real[i])
            s = 0
            """for i in range(len(accuracy)):
                s += accuracy[i]"""
            # print("accuracy is ", s / len(accuracy) * 100, "%", sep="")
            return accuracy

    def convert_field(self, field):
        pole = []
        for i in range(self.heigth):
            a = []
            for j in range(self.length):
                a.append(field[i * self.length + j])
            pole.append(a)
        return pole

    def create_data(self, arr):
        if len(arr) == self.size:
            self.in_data.append(arr)
        else:
            wordlist = [-3, -2, -1, 0, 1, 2, 3]
            array = []
            for i in range(len(wordlist)):
                array = arr.copy()
                array.append(wordlist[i])
                self.create_data(array)
                array = []

    def create_answers(self):
        fighter = Fighter()
        # print("answers creating")
        for i in range(len(self.in_data)):
            pole = self.convert_field(self.in_data[i])
            # print(self.in_data[i], " > ", pole)
            self.out_data.append(fighter.get_data(pole))
            if i % 50000 == 0:
                print(i, self.out_data[len(self.out_data) - 1])
        # print("answers created")

    wordlist = [-3, -2, -1, 0, 1, 2, 3]

    def create_special_answers(self):
        fighter = Fighter()
        # print("answers creating")
        for i in range(len(self.in_data)):
            pole = self.convert_field(self.in_data[i])
            # print(self.in_data[i], " > ", pole)
            self.out_data.append(fighter.get_data(pole))
            if i % 50000 == 0:
                print(i, self.out_data[len(self.out_data) - 1])
        # print("answers created")

    wordlist = [-3, -2, -1, 0, 1, 2, 3]

    def create_data_small(self, arr):
        if len(arr) == self.size:
            self.in_data.append(arr)
            self.in_rate.append(self.rater.get_rating(self.convert_field(arr)))
            if len(self.in_data) % 50000 == 0:
                print(len(self.in_data), self.in_data[len(self.in_data) - 1], self.in_rate[len(self.in_rate) - 1])
            return
        y = len(arr) // self.length
        x = len(arr) - y * self.length
        if x <= max(0, int(self.length / 2 - 1)):
            for i in range(3, 7):
                array = arr.copy()
                array.append(self.wordlist[i])
                self.create_data_small(array)
        elif x >= min(self.length - 1, int((self.length + 1) / 2)):
            for i in range(4):
                array = arr.copy()
                array.append(self.wordlist[i])
                self.create_data_small(array)
        else:
            array = arr.copy()
            array.append(self.wordlist[3])
            self.create_data_small(array)

    def get_special_data(self, arr, arr_input, available):
        if len(arr) == self.size:
            self.in_special.append(arr)
            # print(arr, self.convert_field(arr))
            self.rate_special.append(self.rater.get_rating(self.convert_field(arr)))
            # if len(self.in_special) % 50000 == 0:
            #     print(len(self.in_data), self.in_data[len(self.in_special) - 1], self.rate_special[len(self.in_rate) - 1])
            return
        # if len(arr) < len(arr_input):
        #     arr = arr_input.copy()
        y = len(arr) // self.length
        x = len(arr) - y * self.length
        # print(arr)
        # if x <= max(0, int(self.length / 2 - 1)):
        #     for i in range(3, 7):
        #         array = arr.copy()
        #         array.append(self.wordlist[i])
        #         self.get_special_data(array, arr_input)
        #     return
        if x <= max(0, int(self.length / 2 - 1)):
            arr.append(arr_input[(len(arr_input) // self.heigth) * y + x])
            self.get_special_data(arr, arr_input, available)
        elif x >= min(self.length - 1, int((self.length + 1) / 2)):
            for i in range(3):
                if available > 0:
                    array = arr.copy()
                    array.append(self.wordlist[i])
                    self.get_special_data(array, arr_input, available - 1)
            array = arr.copy()
            array.append(self.wordlist[3])
            self.get_special_data(array, arr_input, available)
        else:
            array = arr.copy()
            array.append(self.wordlist[3])
            self.get_special_data(array, arr_input, available)

    def add_stat(self, array):
        if len(self.accuracies) != 0:
            if len(self.name) == 0:
                array.append(["Unnamed", self.accuracies])
            else:
                array.append([self.name, self.accuracies])
        return array
