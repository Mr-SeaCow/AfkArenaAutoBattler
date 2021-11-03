# ./Classes/Util
import numpy as np

def npToStr(npAra):
    return str(list(np.reshape(np.asarray(npAra), (1, np.size(npAra)))[0]))[1:-1]