from sklearn.datasets import load_iris

def datasets_demo():
    # sklearn数据集更新
    # 获取数据
    
    iris = load_iris()
    print ("莺尾花数据集：\n", iris)
    print ("查看数据集描述：\n", iris["DESCR"])

    return None

if __name__ == "__main__":
    datasets_demo()