#!/usr/bin/python
# python run_booksim.py <directory to injection file>


import os, re, glob, sys, math

# Extract command line arguments
inj_rate_dir = sys.argv[1]

# Initialize dictionary to hold latency values
latency_dict = dict()

# Get a list of all files in directory
files = glob.glob(inj_rate_dir + '/*txt')

# Initialize file counter
file_counter = 0

# Create directory to store config files
os.system('mkdir -p ./logs/configs')

# Iterate over all files
for file in files :

    # Increment file counter
    file_counter += 1

    print('[ INFO] Processing file ' + file + ' ...')

    # Extract file name without extension and absolute path from filename
    run_name = os.path.splitext(os.path.basename(file))[0]

    # Extract first line of file
    line1 = os.popen('head -1 ' + file).read()

    # Extract size of mesh
    line1  = line1.strip()
    values = line1.split()
    size   = int(math.sqrt(len(values)))
    
    # Open read file handle of config file
    fp = open('./htree_mesh_comp/mesh_config', 'r')

    # Set path to config file
    config_file = './logs/configs/' + run_name + '_mesh_config'

    # Open write file handle for config file
    outfile = open(config_file, 'w')

    # Iterate over file and set size of mesh in config file
    for line in fp :
        
        line = line.strip()
        
        # Search for pattern
        matchobj = re.match(r'^k = ', line)

        # Set size of mesh if line in file corresponds to mesh size
        if matchobj :
            line = 'k = ' + str(size) + ';'

        # Write config to file
        outfile.write(line + '\n')

    # Close file handles
    fp.close()
    outfile.close()

    # Set path to log file
    log_file = './logs/' + run_name + '.log'

    # Copy injection rate matrix file
    os.system('cp ' + file + ' ./inj_rate.txt')

    # Run Booksim with config file and save log
    booksim_command = './booksim ' + config_file + ' > ' + log_file
    os.system(booksim_command)

    # Grep for packet latency average from log file
    latency = os.popen('grep "Packet latency average" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()

    print('[ INFO] Latency: ' + latency +'\n')

    # Add key, value to dictionary
    latency_dict[run_name] = latency

    # Stop if 3 files are read
    #if file_counter == 3:
    #    break

# Open output file handle
outfile = open('./logs/booksim_latency_mesh.csv', 'w')

# Write latencies to CSV
for index in range(file_counter) :
    run_name = 'inj_rate_' + str(index+1)
    outfile.write(latency_dict[run_name] + '\n')
outfile.close()
