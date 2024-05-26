# run command for every file
requirements = (OpSysVer == 2204)
universe = vanilla
notification = Complete
notify_user = vs221@ic.ac.uk
initialdir = /homes/vs221/Cryptic-Crossword-Reverse-Dictionary/
executable = /homes/vs221/Cryptic-Crossword-Reverse-Dictionary/run.sh
arguments = $(item) $(Process)

output = $(item)_$(Process).out
error = $(item)_$(Process).err
log = file.log

# Setting environment variables
environment = "HOME=/homes/vs221 PATH=/homes/vs221/.local/bin:/usr/bin:/bin"

queue 20 item matching files configs/config0/*.txt

