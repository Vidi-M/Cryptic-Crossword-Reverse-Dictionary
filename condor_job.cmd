# run command for every file
requirements = (OpSysVer == 2204)
universe = vanilla
notification = Complete
notify_user = vs221@ic.ac.uk
initialdir = /homes/vs221/Cryptic-Crossword-Reverse-Dictionary/
executable = /homes/vs221/Cryptic-Crossword-Reverse-Dictionary/run.sh
arguments = --config $(item)
output = $(item).out
error = $(item).err
log = file.log
queue matching files /homes/vs221/Cryptic-Crossword-Reverse-Dictionary/config_test/*.txt
