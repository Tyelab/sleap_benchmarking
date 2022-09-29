# SLEAP Benchmarking for SNL Computing

This directory contains files that perform individual steps for processing sleap workflows as well as attempts at profiling various problems users encounter from within the Tye Lab.

The initial purpose of these benchmarks was to discover the reasons behind substantial workflow slowdowns people were experiencing. In particular, Anousheh's Tryptateam was experiencing workflows that took approximately 4 hours to do while using machines like Tesla and Doritos.

There's helpful information that can be found [here](https://github.com/talmolab/sleap/discussions/833) on the SLEAP Discussions tab. The documentation found there should probably be made as a PR to SLEAP at some point. In summary, by separating out CPU and GPU workflows you end up with dramatically faster performance! It also helps if you use fancier/newer hardware like the A40s in our new nodes.

This documentation will be improved/added to over time, but for now here's a simple breakdown of whats in here. Since the reason this was started was because of performance problems with Anousheh's project, the videos/models contained here are from her data. All of this was performed on Tesla as I haven't had time to test it on different servers/compute nodes yet. Currently these steps must be done individually, but putting it into one unified script that has structured outputs we can investigate would only require something like a quarter of a day to achieve.

## Benchmarking Scripts

### preloading_benchmark.py

To see if there was an issue with the GPU or machine itself, Talmo suggested having a set of preloaded frames into memory that can be fed into the prediction network. This takes 1024 frames and then runs them through predictions on a trained network. This was quite fast and didn't appear to have any slowdowns.

### video_loading_benchmark.py

To see if there was something particularly difficult about reading the videos into memory from both local and remote sources, Talmo suggested just running the sleap loading functions on videos and see how performance differed. The loading speeds for both remote and local speeds were quite fast indeed.

### whole_video_prediction.py

To see if the predictions themselves were slowing down due to some strange piece of the completed workflow, Talmo suggested literally just running the predict function through Python and measuring speed when reading from a local/remote source. One thought was that for some reason the network was becoming saturated or happened to be busy enough to interfere with the workflow and so while performance was fast at first, over time maybe things began to slow down severely. When running predictions alone, things were quite speedy.

### whole_video_tracking.py

To see if the tracking portion was unusually slow, Talmo suggested running the tracker alone and see how well it performed. Tracking is a CPU bound operation that is quite hard to parallelize due to the dependancy of previous timepoints upon the current timepoint. This also performed well on its own.

## Project Specific Troubles

Anousheh's project is currently struggling with a very strange threading problem. You can see a discussion made about it [here](https://github.com/talmolab/sleap/discussions/894#discussioncomment-3329101).  An issue will be made in the near future to further delve into the problem.

I just confirmed with Anousheh the following:
- Occurs intermittently
- No machine is safe from the problem
- Pointing to correct drivers does not protect you
- Occurs only in the *training* portion of SLEAP's workflow.



