#!/usr/bin/python
# python run_booksim.py <directory to injection file>


import os, re, glob, sys, math
import numpy as np

# Extract command line arguments
trace_file_dir = sys.argv[1] #directory name

os.chdir(trace_file_dir)
#mesh_sizes_per_layer = pd.readcsv('mesh_sizes_per_layer.csv')
mesh_sizes_per_layer = np.loadtxt('mesh_sizes_per_layer.csv')
os.chdir('..')

num_layers = len(mesh_sizes_per_layer)

# Initialize dictionary to hold latency values
# latency_dict = dict()

# Get a list of all files in directory
files = glob.glob(trace_file_dir + '/*txt')

# Initialize file counter
file_counter = 0

# Create directory to store config files
os.system('mkdir -p ./logs/configs')

latency = np.zeros(num_layers)

# Iterate over all files
for layer_idx in range(0, num_layers-1):
#for file in files :

    # upward trace file
    upward_file_name = 'trace_file_upward_' + str(layer_idx) + '.txt'

    # downward trace file
    downward_file_name = 'trace_file_downward_' + str(layer_idx) + '.txt'

    # mesh size
    mesh_size = int(mesh_sizes_per_layer[layer_idx])
    
    # Open read file handle of config file
    fp = open('./mesh_config_trace_based', 'r')

    # Set path to config file
    config_file = './logs/configs/layer_' + str(layer_idx) + '_mesh_config'

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
    log_file = './logs/upward_' + str(layer_idx) + '.log'

    # Copy upward trace file
    os.system('cp ' + trace_file_dir + '/' + upward_file_name + ' ./trace_file.txt')

    # Run Booksim with config file and save log
    booksim_command = './booksim ' + config_file + ' > ' + log_file
    os.system(booksim_command)

    # Grep for packet latency average from log file
    #latency = os.popen('grep "Packet latency average" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()
    upward_latency = os.popen('grep "Trace is finished in" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()

    print('[ INFO] Upward Latency: ' + upward_latency +'\n')

    # Set path to log file for downward trace files
    log_file = './logs/downward_' + str(layer_idx) + '.log'

    # Copy upward trace file
    os.system('cp ' + trace_file_dir + '/' + downward_file_name + ' ./trace_file.txt')

    # Run Booksim with config file and save log
    booksim_command = './booksim ' + config_file + ' > ' + log_file
    os.system(booksim_command)

    # Grep for packet latency average from log file
    downward_latency = os.popen('grep "Trace is finished in" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()

    print('[ INFO] Downward Latency: ' + downward_latency +'\n')

    latency[layer_idx] = max(upward_latency, downward_latency)

np.savetxt('logs/latency_mesh.csv', latency, fmt='%i', delimiter=' ')
