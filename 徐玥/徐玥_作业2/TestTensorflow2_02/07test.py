import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
# Convolution2D 是2维卷积
# MaxPooling2D 是2维最大池化
# Flatten 数据扁平化（降维）
from keras.layers import Dense, Dropout, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
# 以前做过类似的 把28×28的图片扁平化为784的长度的数据

# 优化器
# Adam，常用优化器之一
# 大多数情况下，adam速度较快，达到较优值迭代周期较少，
# 一般比SGD效果好
# CNN应用于手写识别

# 载入数据
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# 查看格式
print('x_shape:', x_train.shape)
print('y_shape:', y_train.shape)

# 转化为4维
# 最后一个维度图片深度，1表示黑白，3表示彩色
# rgb是红绿蓝三通道0-255表示各个通道的颜色深度
# （60000,28,28）->(60000,28,28,1) 四维数据 个数、长、宽、深度
x_train = x_train.reshape(-1, 28, 28, 1) / 255.0
x_test = x_test.reshape(-1, 28, 28, 1) / 255.0
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# 定义序列模型
model = Sequential()

# 第一个卷积层
# input_shape 输入平面
# filters 卷积核/滤波器个数
# kernel_size 卷积窗口大小
# strides 步长
# padding padding方式 same/valid 如果为SAME，则输入输出图片大小一致 VALID则图片经过滤波器后可能会变小。
# activation 激活函数
model.add(Convolution2D(
    input_shape=(28, 28, 1),  # 只需要在第一次添加输入平面
    filters=32,
    kernel_size=5,
    strides=1,
    padding='same',
    activation='relu'
))

# 平面大小28x28，用same padding得到的和上一次一样，也是28x28，有32个特征图
# 池化后变成14x14,32个特征图

# 第一个池化层
model.add(MaxPooling2D(
    pool_size=2,  # 池化窗口大小 2x2的窗口
    strides=2,
    padding='same'
))

# 第二个卷积层
# filters=64 kernel_seize=5
model.add(Convolution2D(64, 5, strides=1, padding='same', activation='relu'))

# 第二个卷积层后64个特征图，14x14
# 第二个池化层后64个特征图，7x7

# 第二个池化层
model.add(MaxPooling2D(2, 2, 'same'))

# 把第二个池化层的输出扁平化为1维
# 长度 64x7x7
model.add(Flatten())

# 第一个全连接层
# 1024个神经元
model.add(Dense(1024, activation='relu'))

# Dropout
# 训练时百分之40个神经元不工作
model.add(Dropout(0.4))

# 第二个全连接层
model.add(Dense(10, activation='softmax'))

# 定义优化器
# 学习速率为10的负4次方 默认是0.001
adam = Adam(lr=1e-4)

# 定义优化器，损失函数，训练效果中计算准确率
model.compile(
    optimizer=adam,  # adam优化器
    loss='categorical_crossentropy',  # 损失用交叉熵，速度会更快
    metrics=['accuracy'],  # 计算准确率
)

# 训练
# 六万张，每次训练64张，训练10个周期（六万张全部训练完算一个周期）
model.fit(x_train, y_train, batch_size=64, epochs=8)

# 评估模型
loss, accuracy = model.evaluate(x_test, y_test)

print('\ntest loss', loss)
print('\ntest accuracy', accuracy)

loss, accuracy = model.evaluate(x_train, y_train)

print('\ntrain loss', loss)
print('\ntrain accuracy', accuracy)

# 保存模型
model.save('model.h5') # HDF5文件 pip install h5py
