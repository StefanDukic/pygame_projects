import time
seconds = time.time()

def realsleep(pause):
    if time.time() - seconds > pause:
        seconds = time.time()
        k = True
    else:
        k = False
    return k

print(realsleep(6))

