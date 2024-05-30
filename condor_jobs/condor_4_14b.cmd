# run command for every file
requirements = ((OpSysVer == 2204) && regexp("^(pixel|texel|vertex|ash|beech|ray).*", Name))
universe = vanilla
notification = Complete
notify_user = vs221@ic.ac.uk
initialdir = /homes/vs221/Cryptic-Crossword-Reverse-Dictionary
executable = /homes/vs221/Cryptic-Crossword-Reverse-Dictionary/run.sh
arguments = $(item) $(Process)

output = file/out4/$(Process).out
error = file/err4/$(Process).err
log = file.log

# Setting environment variables
environment = "HOME=/homes/vs221 PATH=/homes/vs221/.local/bin:/usr/bin:/bin"

queue 200 item matching files configs/phi3-14b/config4.txt

