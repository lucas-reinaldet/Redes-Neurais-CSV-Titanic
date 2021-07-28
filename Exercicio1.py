import pandas as pd
import tensorflow as tf
from tensorflow.python.client import device_lib

def get_available_devices():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU' or x.device_type == 'CPU']
from keras import models, layers
from tensorflow.keras.utils import to_categorical

caminho = "titanic/train.csv"

df = pd.read_csv (r'Redes Neurais/' + caminho)

df = df[["Pclass","Sex","Age","SibSp","Parch","Fare","Embarked", "PassengerId","Survived"]]

df['Embarked'] = pd.Categorical(df['Embarked']).codes
df['Sex'] = pd.Categorical(df['Sex']).codes

train_set = df.sample(frac=0.7)
test_set = df[df.PassengerId.isin(train_set.PassengerId)==False]

train_labels = to_categorical(train_set.Survived)
test_labels = to_categorical(test_set.Survived)

train_set =  train_set.iloc[: , :-2]
test_set =  test_set.iloc[: , :-2]

train_set = tf.convert_to_tensor(train_set, dtype=tf.int64) 
test_set = tf.convert_to_tensor(test_set, dtype=tf.int64) 

rows_set, columns_set = train_set.get_shape()
columns_labels = len(train_labels[0])

def media_geometrica(qtd_entrada, qtd_saida):   
    return int(((qtd_entrada * qtd_saida) ** (1/2)) ** (1/2))

camada1 = int(columns_set * 3.14)
camada2 = int(((columns_set + columns_labels) / 2) * 3.14)
# camada3 = media_geometrica(columns_set, columns_labels)

qtd_epochs = 500
percentual_tam_total = 0.05
tamanho_lotes = int(df.index.max() * percentual_tam_total)

# elu
# exponential
# gelu
# hard_sigmoid
# linear
# relu
# selu
# sigmoid
# softmax
# softplus
# softsign
# swish

tipo_ativacao_inicial = 'softplus'
tipo_ativacao_interna = 'softplus'
tipo_ativacao_saida = 'hard_sigmoid'

network = models.Sequential()
# 50 = identifica a quantidade de neuronios
network.add(layers.Dense(camada1,activation=tipo_ativacao_inicial, input_shape=(columns_set,)))
network.add(layers.Dense(camada2,activation=tipo_ativacao_interna))
# network.add(layers.Dense(camada3,activation='relu'))

network.add(layers.Dense(columns_labels, activation=tipo_ativacao_saida))
network.summary()

# otimizador = 'Adadelta'
# otimizador = 'Adagrad'
# otimizador = 'Adam'
# otimizador = 'Adamax'
# otimizador = 'FTRL'
# otimizador = 'NAdam'
# otimizador = 'RMSprop'
otimizador = 'SGD'

# , steps_per_execution=3
# A execução de vários lotes em uma única chamada tf.function pode melhorar muito o 
# desempenho em TPUs ou pequenos modelos com uma grande sobrecarga do Python.
network.compile(optimizer=otimizador,loss='categorical_crossentropy', metrics=['accuracy'])

history = network.fit(train_set, 
                      train_labels, 
                      epochs= qtd_epochs, 
                      batch_size=tamanho_lotes,
                      # 0 = silent, 1 = progress bar, 2 = one line per epoch
                      verbose=1,
                      # validation_split= 0.7 #,
                      validation_data=(test_set,test_labels)
                      )

test_loss, test_acc = network.evaluate(test_set, test_labels)
print('test_acc: ', test_acc)

import matplotlib.pyplot as plt
history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']

epochs = range(1, len( history_dict['loss']) + 1)
plt.plot(epochs, loss_values, 'bo', label='Training Loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation Loss')
plt.title(caminho + " - Training and Validation Loss" +
          " - otimizador = " + otimizador + 
          " \n- tipo_ativacao_inicial = " + tipo_ativacao_inicial +
          " - tipo_ativacao_interna = " + tipo_ativacao_interna +
          " - tipo_ativacao_saida = " + tipo_ativacao_saida +
          " \n- camada 1 = " + str(camada1) + 
          " - camada 2 = " + str(camada2) + 
          # " - camada3 = " + str(camada3) + 
          " Epochs = " + str(qtd_epochs))
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

#plt.clf()
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']

plt.plot(epochs, acc_values, 'bo', label='Training Acc')
plt.plot(epochs, val_acc_values, 'b', label='Validation Acc')
plt.title(caminho + " - Training and Validation Accuracy" + 
          " - otimizador = " + otimizador + 
          " \n- tipo_ativacao_inicial = " + tipo_ativacao_inicial +
          " - tipo_ativacao_interna = " + tipo_ativacao_interna +
          " - tipo_ativacao_saida = " + tipo_ativacao_saida +
          " \n- camada 1 = " + str(camada1) + 
          " - camada 2 = " + str(camada2) + 
          # " - camada3 = " + str(camada3) + 
          " Epochs = " + str(qtd_epochs))
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()
