# run command for every file
universe = vanilla
notification = Complete
notify_user = vs221@ic.ac.uk
executable = /homes/vs221/Cryptic-Crossword-Reverse-Dictionary/run.sh
arguments = --config $(item)
output = $(item).out
log = file.log
queue matching files config_test/*.txt