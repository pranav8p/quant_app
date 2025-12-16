import seaborn as sns
import matplotlib.pyplot as plt

def correlation_heatmap(df):
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, ax=ax, cmap="coolwarm")
    return fig
