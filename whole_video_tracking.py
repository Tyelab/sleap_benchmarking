import sleap
from time import perf_counter

# Load predictions
labels = sleap.load_file("/scratch/sleap_benchmark/20220628_Con4_3934R_M_RL.mp4.predictions.slp")

# Here I'm removing the tracks so we just have instances without any tracking applied.
for instance in labels.instances():
    instance.track = None
labels.tracks = []
print(labels)

# Create tracker
tracker = sleap.nn.tracking.Tracker.make_tracker_by_name(
    # General tracking options
    tracker="flow",
    track_window=3,

    # Matching options
    similarity="instance",
    match="greedy",
    min_new_track_points=1,
    min_match_points=1,

    # Optical flow options (only applies to "flow" tracker)
    img_scale=0.5,
    of_window_size=21,
    of_max_levels=3,

    # Pre-tracking filtering options
    target_instance_count=2,
    pre_cull_to_target=True,
    pre_cull_iou_threshold=0.8,

    # Post-tracking filtering options
    post_connect_single_breaks=True,
    clean_instance_count=0,
    clean_iou_threshold=None,
)

t0 = perf_counter()
tracked_lfs = []
for lf in labels:
    lf.instances = tracker.track(lf.instances, img=lf.image)
    tracked_lfs.append(lf)
tracked_labels = sleap.Labels(tracked_lfs)
print(tracked_lfs)

end = perf_counter() - t0

print(len(tracked_lfs)/end)

# Tracking is slowest in the workflow, CPU only, not parallelized, hard to do, to be replaced
# by adding a layer to the network eventually that learns the trajectories of stuff
# very cool 
