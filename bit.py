from sklearn.datasets import make_classification
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
# 设置 matplotlib 配置，使用支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
matplotlib.rcParams['axes.unicode_minus'] = False    # 正确显示负号
# 增加 n_informative 的值以支持更多类别
X, y = make_classification(n_samples=1000, n_features=20, n_informative=3, n_redundant=10, n_classes=6, n_clusters_per_class=1, random_state=42)

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练随机森林分类器
classifier = RandomForestClassifier(random_state=42)
classifier.fit(X_train, y_train)

# 预测测试集结果
y_pred = classifier.predict(X_test)

# 计算混淆矩阵
cm = confusion_matrix(y_test, y_pred)

# 使用 seaborn 绘制混淆矩阵
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["历史风情", "当地特色", "博物馆", "游乐中心", "现代风情", "动物园"], yticklabels=["历史风情", "当地特色", "博物馆", "游乐中心", "现代风情", "动物园"])
plt.xlabel('预测类别')
plt.ylabel('实际类别')
plt.title('多类分类混淆矩阵')
plt.show()
