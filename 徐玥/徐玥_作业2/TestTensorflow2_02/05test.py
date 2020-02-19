import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout  # 在这里导入dropout
from keras.optimizers import SGD

# Dropout
# 使用dropout是要改善过拟合，将训练和测试的准确率差距变小
# 训练集，测试集结果相比差距较大时，过拟合状态
# 使用dropout后，每一周期准确率可能不高反而最后一步提升很快，这是训练的时候部分神经元工作，而最后的评估所有神经元工作
# 正则化同样是改善过拟合作用
# Softmax一般用在神经网络的最后一层

# 载入数据
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# 查看格式
print('x_shape:', x_train.shape)
print('y_shape:', y_train.shape)
x_train = x_train.reshape(x_train.shape[0], -1) / 255.0
x_test = x_test.reshape(x_test.shape[0], -1) / 255.0
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# 创建模型
# 偏执值初始值设为zeros（默认为zeros）
model = Sequential([
    Dense(units=200, input_dim=784, bias_initializer='zeros', activation='tanh'),  # 双曲正切激活函数
    Dropout(0.4),  #百分之40的神经元不工作
    Dense(units=100, bias_initializer='zeros', activation='tanh'),  # 双曲正切激活函数 只有第一层需要输入input_dim
    Dropout(0.4),  #百分之40的神经元不工作
    Dense(units=10, bias_initializer='zeros', activation='softmax') # softmax一般是最后一层输出
])
# 定义优化器
sgd = SGD(lr=0.2)

# 定义优化器，损失函数，训练效果中计算准确率
model.compile(
    optimizer=sgd,
    loss='categorical_crossentropy',  # 损失用交叉熵，速度会更快
    metrics=['accuracy'],
)

# 训练
# 六万张，每次训练32张，训练10个周期（六万张全部训练完算一个周期）
model.fit(x_train, y_train, batch_size=32, epochs=10)

# 评估模型
loss, accuracy = model.evaluate(x_test, y_test)

print('\ntest loss', loss)
print('\ntest accuracy', accuracy)

loss, accuracy = model.evaluate(x_train, y_train)

print('\ntrain loss', loss)
print('\ntrain accuracy', accuracy)
# 打印用训练集测试结果，看看是否过拟合
