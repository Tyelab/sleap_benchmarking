# Benchmarking script for preloading a small chunk of videos that are
# predicted upon.
# Written by Talmo Periera, see https://github.com/talmolab/sleap/discussions/833#discussioncomment-3311586
# This is to see if there is something specific to the GPU/machine that
# we're trying to run SLEAP on. Some users are experiencing slow runtimes
# where the GPU is barely being utilized during sleap-track and their inference
# speeds are quite low (15-30 FPS) when they should be nice and speedy!

import sleap
import numpy as np
from time import perf_counter

video = sleap.load_video("/scratch/sleap_benchmark/20220628_Con4_3934R_M_RL.mp4")

# This example video/model pair was generated using a top-down approach
# which requires two model paths in a list:
predictor = sleap.load_model([
    "/nadata/snlkt/spb_psilicon/Pilot_BehParameters/SLEAP/SLEAP_phase4/models/220801_174806.centroid.n=2092",
    "/nadata/snlkt/spb_psilicon/Pilot_BehParameters/SLEAP/SLEAP_phase4/models/220801_181533.centered_instance.n=2092"
    ],
    batch_size=32,
    )

# Preload images
imgs = video[:1024]

predictor.predict(imgs[:16])  # warmup

for _ in range(3):  # do multiple trials
    t0 = perf_counter()
    predictor.predict(imgs)
    elapsed = perf_counter() - t0

    fps = len(imgs) / elapsed
    print(fps)