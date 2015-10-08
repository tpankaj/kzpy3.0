"""
animate random matrix
"""
from kzpy3.vis import *
from  matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(7,7))
    
rnd = np.random.random((100,512,512))
def update2(frame_number):
  plt.clf()
  mi(rnd[randint(100),:,:])

animation = FuncAnimation(fig, update2, interval=30, repeat=True)
plt.show()
