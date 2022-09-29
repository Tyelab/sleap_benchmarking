# Some users are experiencing slow video IO over our cluster network (probably)
# This script just loads first a local scratch space video and times how long it takes
# to read through each batch of frames. It will then do it from remote
# storage to see how long it takes to access the frames.

import sleap
from time import perf_counter
import numpy as np


video = sleap.load_video("/scratch/spb_benchmark/20220628_Con4_3934R_M_RL.mp4")
batch_size = 16
n_frames = len(video) # or len(video), but this might take a while
local_fps = []
for i0 in range(0, n_frames, batch_size):
    t0 = perf_counter()
    i1 = min(i0 + batch_size, len(video))
    imgs = video[i0:i1]
    elapsed = perf_counter() - t0
    fps = len(imgs) / elapsed
    local_fps.append(fps)

print("Testing remote...")

remote = sleap.load_video("/snlkt/spb_psilicon/Pilot_BehParameters/Videos_RawData/FFBatch/20220619_Con1_3934R_M_RL.mp4")
remote_fps = []
nframes = len(remote)
for i0 in range(0, n_frames, batch_size):
    t0 = perf_counter()
    i1 = min(i0 + batch_size, len(video))
    imgs = remote[i0:i1]
    elapsed = perf_counter() - t0
    fps = len(imgs) / elapsed
    print("REMOTE: ", fps)
    remote_fps.append(fps)

print(np.mean(np.array(local_fps)))
print(np.mean(np.array(remote_fps)))

