import subprocess

def get_gpu_memory():
    """
    Utility function for getting available GPUs on a machine and determining
    if the card is available for running a SLEAP GPU workload (ie predict, train)

    See below for where this code basically comes from, just without as many comments...

    """

    # Subprocessing asks for a command in a list form. We'll be using the NVIDIA SMI tool
    # or the NVIDIA System Management Interface, which is a command line tool for interacting
    # with the available GPUs on a computer. There are some libraries out there that do this, but
    # they don't seem to all play nice on Windows, so manually processing the outputs seems
    # necessary.

    # Create a subprocess, meaning a program that will run in the background, from the main script
    # Our command arguments mean:
    # 1. nvidia-smi: Run the nvidia-smi command
    # 2. "--query-gpu=": How you ask nvidia-smi to ask about specific GPU properties
    # 3. index: Zero-indexed GPU ID for the machine. I'm not sure if the index alone is consistent. The docs say
    # that if there's a hard reset/reboot of the machine it could change, but that shouldn't happen during a run
    # anyways...
    # 4. memory.free: Free memory in megabytes
    # 5. memory.total: Total memory on the card in megabytes
    # 6. "--format=csv": How the data is displayed to a terminal for you I think/can be stored to file if you want
    command = ["nvidia-smi", "--query-gpu=index,memory.free,memory.total", "--format=csv"]

    # Using subprocess.run, the command above will be executed in the background! We tell the subprocess to run
    # and also capture the output of the command which will return a bytestring (ie b'message') to the memory_poll
    # variable
    memory_poll = subprocess.run(
        command,
        capture_output=True
        )

    # Grab the stdout, or standard out, from the subprocess call to nvidia-smi. This basically
    # just stores the output of our subprocess to a variable that we can do things to!
    subprocess_result = memory_poll.stdout

    # You can do this on the same line, but for explaination sake I separated it out to another
    # line.
    # The output of nvidia-smi is passed as an ascii encoded byte string. The subprocess_result
    # variable itself is a bytestring! So we can the decode method on directly and specify "ascii"
    # as the encoding of the data. Each line that's normally displayed as a pretty row/column format
    # is split up by a newline character, or the "\n" character. So we split up the decoded string by
    # these newline characters. Next, we only want useful information in the output list that split
    # gives us. The final line of nvidia-smi is an empty string for some reason, so by getting everything
    # up to the last element we remove it from the output! Next, we don't need the header of the csv
    # that says what the variables are since they won't be displayed to the user. These are the first values
    # in the list, so we can ignore them by slicing past them!
    memory_string = subprocess_result.decode("ascii").split("\n")[:-1][1:]

    # We want to be able to parse out which card has memory available. Another way of doing this would be
    # to see if the card has any working processes on it, but for now memory seems like a reasonable
    # thing to select. So a dictionary is made where the keys will be the ID of the card (remember,
    # zero indexed!) and the value will be the difference between total and available memory.
    memory_dict = {}

    # The split and slicing we did above makes it so we have each row in its own list. So for
    # each row in the decoded string...
    for row in memory_string:

        # Get the gpu ID, which is the first element of the list we make with split here
        gpu_id = row.split(",")[0]
        # Get the available amount of memory, the second element of the list made with split here
        available = row.split(",")[1]
        # Get total amount of memory, the final element of the list made with split here
        total = row.split(",")[2]

        # Allegedly, using string translate methods is faster than using a regex (not that it matters here...)
        # so make a "translate" map that will replace the megabyte characters (MiB) with equivalently sized
        # length of spaces (3 letters in MiB, so 3 spaces)
        available_translator = available.maketrans("MiB", "   ")
        total_translator = total.maketrans("MiB", "   ")

        # Perform the translation method and then strip the spaces from the resulting strings
        available_memory = available.translate(available_translator).strip()
        total_memory = total.translate(total_translator).strip()

        # Add the gpu_id as the key for the dictionary and subtract the total/available memory
        # after converting those strings into integers. A value of 0 indicates that the card
        # has all of it's memory availble! If all the memory is unallocated, we can then use
        # that to spawn off SLEAP jobs to the available graphics cards (hopefully...)
        memory_dict[gpu_id] = round(int(available_memory) / int(total_memory), 4)

    return memory_dict


memory = get_gpu_memory()

print(memory)