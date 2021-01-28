# roll20-statistics
This is a CLI tool for generating statistics for d20 rolls using Roll20 chat logs. Right now, statistics are output directly to the command line.

## Requirements
Python 3.7+

## Usage
In the logs folder, modify the names.csv file to match your own players' names. The player's real name goes in the first column. All of their associated names in Roll20 go in the following columns. The statistics for all of their associated names will be aggregated under their real name. Modify that file using notepad rather than Excel.

Also in the logs folder, include a .txt file with the Roll20 chat logs copy pasted into it.

Run main.py on the command line and it will have you select the relevant names and chat log files. It will then generate statistics based on the given files.