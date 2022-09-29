# Determining encoding of videos in case they're not using H264 encoding
# which is recommended by Talmo for best use of SLEAP. Does not currently check for
# pixel format, presets, etc. Only for whether or not H264 was used.
# SLEAP runs fine on a windows machine, but we're running into an issue on Linux
# that appears to be related to ffmpeg not being able to open up videos encoded
# via HEVC (synonymous with H265?) on Linux systems. This means something is wrong
# with the linux deployment/server. ffmpeg complied incorrectly maybe. In
# the meantime, re-encoding could be a band-aid.

# Jeremy Delahanty 8/23/22

# Import PIPE to receive standard out from ffprobe subprocess
from asyncio.subprocess import PIPE

# Import subprocess to initiate ffprobe/ffmpeg iff user wants it
import subprocess

# Pathlib for globbing
from pathlib import Path

# TODO: Make this an argument in an argparser or something for more general use
base_dir = Path("/snlkt/ast/SLEAP/SLEAP_VIDS")

# Assume that people have all videos in a single directory for a project which seems
# to be how people are currently running sleap in general
# Not sure why I used a dictionary, this part wasn't really necessary I don't think...
# Dictionary comprehension to make keys of folders with empty list of videos that will
# be populated later.
subfolders = {folder : [] for folder in base_dir.glob("*") if folder.is_dir()}

# Make empty dictionary that will be receiving encodings found in the subdirectories
# as keys with video paths as their values
encodings = {}


for folder in subfolders.keys():
    # Grab all .mp4 videos, should probably make something more general that can receive
    # any video extension, but most people are recording using mp4 I think...
    # Add list of all videos to each dictionary subfolder entry
    subfolders[folder] = [vid for vid in folder.glob("*.mp4")]

    for vid in subfolders[folder]:

        # Try to execute ffprobe on each video for each folder
        # See stack-overflow here for this trick:
        # https://stackoverflow.com/questions/2869281/how-to-determine-video-codec-of-a-file-with-ffmpeg
        try:
            cmd = [f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {str(vid)}"]
            # Open the subprocess in the shell, capture standard out in a PIPE and decode the byte string into text
            p = subprocess.Popen(cmd, shell=True, stdout=PIPE, text=True)
            # Grab subprocess stdout and stderr into these variables
            out, err = p.communicate()
            # The output of this command is just the encoder used in the video
            # It has a newline/blank space in it so strip any useless characters
            encoding = out.strip()
            # If the encoding isn't already logged and also not empty  (result of spaces in one of Fergil's filenames)
            # both create that key and also add the video to the list
            if encoding not in encodings.keys() and encoding != "":
                encodings[encoding] = [vid]
            # Let Fergil know which video has the weird spaces in it if the encoding is empty
            # Capturing this with stderr is the right way to do this, but I'm being lazy...
            elif encoding == "":
                print("ERROR: PROBABLY FILENAME ISSUE, REMOVE SPACES")
                print(vid)
                print("============")
            # If the encoding is logged/not empty, add the video to the list held by the encoding key
            # in the encoding dict
            else:
                encodings[encoding].append(vid)

        except:
            # TODO: If there's a problem with something capturing the proper exception
            # should be done and logged/printed out for the user to know about...
            print("Unknown error")

# For each encoding found...
for encoding in encodings.keys():
    # If the encoding isn't h264, which is what Talmo recommends
    if encoding != "h264":
        # Tell the user how many + which videos aren't encoded with h264
        print("FOUND", len(encodings[encoding]), "VIDEOS ENCODED BY", encoding)
        for video in encodings[encoding]:
            print(video.name)
        
        # Ask the user if they want to re-encode according to Talmo's recommended settings
        encode = input("Re-encode via ffmpeg? Y/N ")

        # If the user says "y", re-encode according to recommended setting and have re-encoded videos
        # appended with _re-encoded
        if encode == "Y" or "y":
            for video in encodings[encoding]:
                output_name = video.parent / str(video.stem + "_re-encoded.mp4")
                cmd = [f"ffmpeg -i {str(video)} -c:v h264 -preset superfast -pix_fmt yuv420p -crf 15 -threads 2 {str(output_name)}"]

                # If Fergil is brave enough to trust my Python programming, he can have all these videos processed simultaneously
                # instead of serially. There's something like 30 videos with HEVC encoding, so you want a machine with 60 threads
                # available. Cheetos should serve this purpose. Just uncomment this next line and it should work...
                p = subprocess.Popen(cmd, shell=True)


print("===================")
print("Goodbye my friend...")
