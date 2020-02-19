import numpy as np
from keras.datasets import mnist  # 将会从网络下载mnist数据集
from keras.utils import np_utils
from keras.models import Sequential  # 序列模型
from keras.layers import Dense
from keras.optimizers import SGD

# MINIST数据集分类

# 载入数据 不是很大 大约十几兆
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# x y 分别为数据与标签
# 查看格式
# （60000,28,28）
print('x_shape:', x_train.shape)
# （60000）6万个数据 图片2对应标签2
print('y_shape:', y_train.shape)
# （60000,28,28）->(60000,784)
# 行数60000，列-1表示自动设置
# 除以255是做数据归一化处理
x_train = x_train.reshape(x_train.shape[0], -1)/255.0   # 转换数据格式
x_test = x_test.reshape(x_test.shape[0], -1)/255.0  # 转换数据格式
# label标签转换成 one  hot 形式
y_train = np_utils.to_categorical(y_train, num_classes=10)   # 分成10类
y_test = np_utils.to_categorical(y_test, num_classes=10)    # 分成10类


# 创建模型，输入784个神经元，输出10个神经元
# 偏执值初始值bias_initializer设为1（默认为0）
# activation='softmax' 输出转成概率
model = Sequential([
    Dense(units=10, input_dim=784, bias_initializer='one', activation='softmax')
])

# 定义优化器
# 学习速率为0.2
sgd = SGD(lr=0.2)

# 定义优化器，损失函数，训练效果中计算准确率
model.compile(
    optimizer=sgd,  # sgd优化器
    loss='mse',  # 损失用均方差
    metrics=['accuracy'],  # 计算准确率
)

# 训练（不同于之前，这是新的训练方式）
# 六万张，每次训练32张，训练10个周期（六万张全部训练完算一个周期）
model.fit(x_train, y_train, batch_size=32, epochs=10)
# epochs 迭代周期

# 评估模型
# 用了测试集
loss, accuracy = model.evaluate(x_test, y_test)

print('\ntest loss', loss)
print('accuracy', accuracy)