import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

'''
	@ brief		生成样本数据
	@ param		样本规模
	@ return	
'''
def generate_data(n_samples):
    np.random.seed(0)
    x = np.random.uniform(-2*np.pi, 2*np.pi, n_samples)
    y = np.sin(x)
    return x, y

# 定义神经网络模型
class ReLU_Net(nn.Module):
    # 定义三个线性层，两个RelU层连接作隐藏层
    def __init__(self):
        super(ReLU_Net, self).__init__()
        self.fc1 = nn.Linear(1, 64)
        self.fc2 = nn.Linear(64, 16)
        self.fc3 = nn.Linear(16, 1)
        self.relu = nn.ReLU()

    # 前向传播
    def forward(self, x):
        h1 = self.relu(self.fc1(x))
        h2 = self.relu(self.fc2(h1))
        y = self.fc3(h2)
        return y

'''
	@ brief			训练神经网络
	@ param
		model		模型
		criterion	损失函数
		optimizer	优化器
		x_train		特征
		y_train		标签
		epochs		训练轮次
'''
def train(model, criterion, optimizer, x_train, y_train, epochs):
    model.train()
    for epoch in range(epochs):
        inputs = torch.tensor(x_train, dtype=torch.float32).unsqueeze(1)
        targets = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        # 每100轮打印一次训练结果
        if (epoch+1) % 100 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

'''
	@ brief			得到验证结果
	@ param
		model		模型
		x_test		特征
	@ return		预测值
'''
def test(model, x_test):
    model.eval()
    with torch.no_grad():
        inputs = torch.tensor(x_test, dtype=torch.float32).unsqueeze(1)
        outputs = model(inputs)
        predictions = outputs.squeeze(1).numpy()
    return predictions

# 生成数据集(1000)
x_data, y_data = generate_data(1000)

# 随机划分训练集(800)和测试集(200)
indices = np.random.permutation(len(x_data))
train_indices, test_indices = indices[:800], indices[800:]
x_train, y_train = x_data[train_indices], y_data[train_indices]
x_test, y_test = x_data[test_indices], y_data[test_indices]

# 定义神经网络模型、损失函数和优化器
model = ReLU_Net()
criterion = nn.MSELoss()                                # 均方误差损失函数
optimizer = optim.Adam(model.parameters(), lr=0.001)    # Adam优化器

# 训练模型
train(model, criterion, optimizer, x_train, y_train, epochs=1000)

# 使用测试集验证模型拟合效果
predictions = test(model, x_test)

# 绘制结果
plt.scatter(x_test, y_test, color='blue', label='True Function')
plt.scatter(x_test, predictions, color='red', label='Predictions')
plt.title('Fitting Sin Function with ReLU Neural Network')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()