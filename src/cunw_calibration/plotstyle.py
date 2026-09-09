import matplotlib.pyplot as plt

def savefig(path):
    plt.tight_layout(); plt.savefig(path,dpi=300,bbox_inches="tight"); plt.close()
