import sleap
from time import perf_counter

print("LOCAL TEST")
video = sleap.load_video("/scratch/sleap_benchmark/20220628_Con4_3934R_M_RL.mp4")

predictor = sleap.load_model([
    "/nadata/snlkt/spb_psilicon/Pilot_BehParameters/SLEAP/SLEAP_phase4/models/220801_174806.centroid.n=2092",
    "/nadata/snlkt/spb_psilicon/Pilot_BehParameters/SLEAP/SLEAP_phase4/models/220801_181533.centered_instance.n=2092"
    ],
    batch_size=64
    )

t0 = perf_counter()
predictor.predict(video)
elapsed = perf_counter() - t0

fps = len(video) / elapsed
print(fps)

print("REMOTE TEST")

video = sleap.load_video("/snlkt/spb_psilicon/Pilot_BehParameters/Videos_RawData/FFBatch/20220628_Con4_3934R_M_RL.mp4")

t0 = perf_counter()
predictor.predict(video)
elapsed = perf_counter() - t0

fps = len(video) / elapsed
print(fps)