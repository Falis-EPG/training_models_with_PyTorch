# -*- coding: utf-8 -*-
"""TrainingModels.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DiH8rqJI0-9DunGt5OLkjvo8eIWY_l8y
"""

import torch
from torch import nn
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from torch import optim
from torchvision import datasets
from torchvision import transforms
from torch.utils.data import DataLoader

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

print(device)

"""# **Treinamento Básico para classificação de Vinhos!**"""

wine = datasets.load_wine()
data = wine.data
target = wine.target

print(data.shape, target.shape)
print(wine.feature_names, wine.target_names)

class WineClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, out_size):
        super(WineClassifier, self).__init__()

        self.hidden = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.out = nn.Linear(hidden_size, out_size)
        self.softmax = nn.Softmax()

    def forward(self, X):

        feature = self.relu(self.hidden(X))
        output = self.softmax(self.out(feature))

        return output

input_size = data.shape[1]
hidden_size = 32
out_size = len(wine.target_names)

net = WineClassifier(input_size, hidden_size, out_size).to(device)

print(net)

criterion = nn.CrossEntropyLoss().to(device)

Xtns = torch.from_numpy(data).float()
Ytns = torch.from_numpy(target)

Xtns = Xtns.to(device)
Ytns = Ytns.to(device)

print(Xtns.dtype, Ytns.dtype)

pred = net(Xtns)

print(pred.shape, Ytns.shape)
print(pred[0].data, Ytns[0].data)

loss = criterion(pred[:50], Ytns[:50])
print(loss)

"""# **Treinamento Básico para predição de Diabetes!**"""

diabetes = datasets.load_diabetes()
data = diabetes.data
target = diabetes.target

print(data.shape, target.shape)
print(data[0], target[0])

class WineClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, out_size):
        super(WineClassifier, self).__init__()

        self.hidden = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.out = nn.Linear(hidden_size, out_size)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, X):

        feature = self.relu(self.hidden(X))
        output = self.softmax(self.out(feature))

        return output

input_size = data.shape[1]
hidden_size = 32
out_size = 1

net = WineClassifier(input_size, hidden_size, out_size).to(device)

criterion = nn.MSELoss().to(device)
Xtns = torch.from_numpy(data).float().to(device)
Ytns = torch.from_numpy(target).float().to(device)

print(Xtns.shape, Ytns.shape)

pred = net(Xtns)

loss = criterion(pred.squeeze(), Ytns)
print(loss.data)

"""# **Otimização de taxa de aprendizado básica com a rede de classificação de vinhos!**"""

features = [0, 9]

wine = datasets.load_wine()
data = wine.data[:, features]
target = wine.target

plt.scatter(data[:, 0], data[:,1], c=target, s=15, cmap=plt.cm.brg)
plt.xlabel(wine.feature_names[features[0]])
plt.ylabel(wine.feature_names[features[1]])

scaler = StandardScaler()
data = scaler.fit_transform(data)

plt.scatter(data[:, 0], data[:,1], c=target, s=15, cmap=plt.cm.brg)
plt.xlabel(wine.feature_names[features[0]])
plt.ylabel(wine.feature_names[features[1]])

input_size = data.shape[1]
hidden_size = 32
out_size = len(wine.target_names)

print(device)

net = nn.Sequential(
    nn.Linear(input_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, out_size),
    nn.Softmax()
)

net = net.to(device)

import numpy as np

def plot_boundary(X, y, model):
  x_min, x_max = X[:, 0].min()-0.1, X[:, 0].max()+0.1
  y_min, y_max = X[:, 1].min()-0.1, X[:, 1].max()+0.1

  spacing = min(x_max - x_min, y_max - y_min) / 100

  XX, YY = np.meshgrid(np.arange(x_min, x_max, spacing),
                       np.arange(y_min, y_max, spacing))

  data = np.hstack((XX.ravel().reshape(-1,1),
                    YY.ravel().reshape(-1,1)))

  # For binary problems
  #db_prob = model(Variable(torch.Tensor(data)).cuda() )
  #clf = np.where(db_prob.cpu().data < 0.5,0,1)

  # For multi-class problems
  db_prob = model(torch.Tensor(data).to(device) )
  clf = np.argmax(db_prob.cpu().data.numpy(), axis=-1)

  Z = clf.reshape(XX.shape)

  plt.contourf(XX, YY, Z, cmap=plt.cm.brg, alpha=0.5)
  plt.scatter(X[:,0], X[:,1], c=y, edgecolors='k', s=25, cmap=plt.cm.brg)

plot_boundary(data, target, net)

#Função de Perda
criterion = nn.CrossEntropyLoss().to(device)

#Otimizador
optmizer = optim.SGD(net.parameters(), lr=1e-3)

X = torch.FloatTensor(data).to(device)
Y = torch.LongTensor(target).to(device)

for i in range(100):
  #Forward
  pred = net(X)
  loss = criterion(pred, Y)

  #backward
  loss.backward()
  optmizer.step()

  if i % 10 == 0:
    plt.figure()
    plot_boundary(data, target, net)

for i in range(100):
  #Forward
  pred = net(X)
  loss = criterion(pred, Y)

  #backward
  loss.backward()
  optmizer.step()

  if i % 10 == 0:
    plt.figure()
    plot_boundary(data, target, net)

for i in range(100):
  #Forward
  pred = net(X)
  loss = criterion(pred, Y)

  #backward
  loss.backward()
  optmizer.step()

  if i % 10 == 0:
    plt.figure()
    plot_boundary(data, target, net)

"""# **Trabalhando com datasets no PyTorch!**"""

args = {
    'batch_size': 20,
    'num_workers': 4,
    'num_classes': 10,
    'lr': 1e-4,
    'weight_decay': 5e-4,
    'num_epochs': 30
}

if torch.cuda.is_available():
  args['device'] = torch.device('cuda')
else:
  args['device'] = torch.device('cpu')

print(args['device'])

train_set = datasets.MNIST('./',
                      train=True,
                      transform=transforms.ToTensor(),
                      download=True)

test_set = datasets.MNIST('./',
                      train=False,
                      transform=transforms.ToTensor(),
                      download=False)

print('Amostras de Treino:' + str(len(train_set)) + '\nAmostras de Teste:'+ str(len(test_set)))

print(type(train_set))
print(type(train_set[0]))

for i in range(3):
  dado, rotulo = train_set[i]

  plt.figure()
  plt.imshow(dado[0])
  plt.title('Rotulo:' + str(rotulo))

train_loader = DataLoader(train_set,
                          batch_size=args['batch_size'],
                          shuffle=True,
                          num_workers=args['num_workers'])

test_loader = DataLoader(test_set,
                          batch_size=args['batch_size'],
                          shuffle=True,
                          num_workers=args['num_workers'])

for batch in train_loader:

  dado, rotulo = batch
  print(dado.size(), rotulo.size())

  plt.imshow(dado[0][0])
  plt.title('Rotulo:' + str(rotulo[0]))

  break

class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, out_size):
        super(MLP, self).__init__()

        self.features = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )
        self.out = nn.Linear(hidden_size, out_size)
        self.softmax = nn.Softmax()

    def forward(self, X):

        X = X.view(X.size(0), -1)

        feature = self.features(X)
        output = self.softmax(self.out(feature))

        return output

input_size = 28 * 28
hidden_size = 128
out_size = 10

net = MLP(input_size, hidden_size, out_size).to(args['device'])

criterion = nn.CrossEntropyLoss().to(args['device'])
optmizer = optim.Adam(net.parameters(), lr=args['lr'], weight_decay=args['weight_decay'])

for epoch in range(args['num_epochs']):
  epoch_loss = []
  for batch in train_loader:
    dado, rotulo = batch
    dado = dado.to(args['device'])
    rotulo = rotulo.to(args['device']) # Transfer rotulo to the device
    pred = net(dado)
    loss = criterion(pred, rotulo)
    epoch_loss.append(loss.cpu().data)
    loss.backward()
    optmizer.step()

  epoch_loss = np.asarray(epoch_loss)

  print('Época %d, Loss: %.4f +/- %.4f' % (epoch, epoch_loss.mean(), epoch_loss.std()))

