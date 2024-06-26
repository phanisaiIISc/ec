#!/usr/bin/python
# python run_booksim.py <directory to injection file>


import os, re, glob, sys, math
import numpy as np

# Extract command line arguments
trace_file_dir = sys.argv[1] #directory name

os.chdir(trace_file_dir)
mesh_dim = np.loadtxt('mesh_sizes.csv')
os.chdir('..')

mesh_size = int(np.ceil(mesh_dim[0]))

# Create directory to store config files
os.system('mkdir -p ./logs/configs')

# Open read file handle of config file
fp = open('./mesh_config_dummy', 'r')

# Set path to config file
config_file = './logs/configs/area_power_mesh_config'

# Open write file handle for config file
outfile = open(config_file, 'w')

# Iterate over file and set size of mesh in config file
for line in fp :
    
    line = line.strip()
    
    # Search for pattern
    matchobj = re.match(r'^k=', line)

    # Set size of mesh if line in file corresponds to mesh size
    if matchobj :
        line = 'k=' + str(mesh_size) + ';'

    # Write config to file
    outfile.write(line + '\n')

# Close file handles
fp.close()
outfile.close()

# Set path to log file for upward trace files
log_file = './logs/area_power' + '.log'

# Run Booksim with config file and save log
booksim_command = './booksim ' + config_file + ' > ' + log_file
os.system(booksim_command)

# Grep for area and energy from log file
#latency = os.popen('grep "Packet latency average" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()
area = os.popen('grep "Total Area" ' + log_file + ' | tail -1 | awk \'{print $4}\'').read().strip()

print('[ INFO] : ' + area +'\n')

power = os.popen('grep "Total Power" ' + log_file + ' | tail -1 | awk \'{print $4}\'').read().strip() 

print('[ INFO] : ' + power +'\n')

# Open output file handle
outfile_area = open('./logs/booksim_area_custom_nn.csv', 'a')
outfile_area.write(area + '\n')
outfile_area.close()
    
# Open output file handle
outfile_power = open('./logs/booksim_power_custom_nn.csv', 'a')
outfile_power.write(power + '\n')
outfile_power.close()
