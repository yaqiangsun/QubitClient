import sys
sys.path.append("./")
from resources.quark.anaylsis.format import powershift_convert
from resources.quark.anaylsis.utils import get_pkl_content
import numpy as np

def convert(path):
    content = get_pkl_content(path)
    data = powershift_convert(content)
    npy_path = path.replace(".pkl", ".npy")
    np.save(npy_path,data)
if __name__ == "__main__":
    convert("tmp/data/powershift/955.pkl")
