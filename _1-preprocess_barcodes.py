import os
import sys
import subprocess
import shutil
import glob

def main(directory):
    # Define paths
    sf = "/LETHE/Members/bins/SeqFilter/bin/SeqFilter"
    sickle = "/LETHE/Members/bins/sickle/sickle"
    BLASTDB = "/LETHE/Members/data/Refs/NCBI/"
    stk = "/LETHE/Members/bins/seqtk/seqtk"
    DBpreclass = "/LETHE/Members/MB/_DBs/its2.global.2023-01-17.curated.tax.mc.add.fa"
    
    # Change to the target directory
    os.chdir(directory)
    threads = 10

    # Clean up and create directories
    if os.path.exists('logs'):
        shutil.rmtree('logs')
    os.makedirs('logs', exist_ok=True)
    os.makedirs('raw', exist_ok=True)
    os.makedirs('fq', exist_ok=True)
    os.makedirs('fa', exist_ok=True)
    os.makedirs('tooshort', exist_ok=True)
    
    # Remove old files
    for filename in glob.glob('*.[fF]*') + glob.glob('*results') + glob.glob('*.out'):
        os.remove(filename)
    
    # Process each .ab1 file
    for file in glob.glob('*.ab1'):
        s = '.'.join(file.split('.')[:-1])
        
        print("\n====================================")
        print(f"Processing sequence {s}")
        print("====================================")
        
        print("... basecalling")
        subprocess.run(['docker', 'run', '-u', f'{os.getuid()}:{os.getgid()}', '-v', f'{os.getcwd()}:/data', 'geargenomics/tracy', 'tracy', 'basecall', '-f', 'fastq', '-o', f'/data/{s}.fq', f'/data/{s}.ab1'])
        
        print("... quality truncation")
        subprocess.run([sickle, 'se', '-f', f'{s}.fq', '-t', 'sanger', '-o', f'{s}.si.fastq', '-q', '25', '-t', 'sanger', '-l', '100'])
        
        size = os.path.getsize(f'{s}.si.fastq')
        if size > 0:
            write_next_line = False

            with open(f'{s}.si.fastq', 'r') as infile, open(f'{s}.si.fa', 'w') as outfile:
                for line in infile:
                    line = line.strip()
                    if line.startswith('@primary'):
                        line = f'>{s}-SI'
                        outfile.write(line + '\n')
                        write_next_line = True  # Enable writing the next line
                    elif write_next_line:
                        outfile.write(line + '\n')
                        break  # Exit after writing the second line
        else:
            for pattern in [f'{s}*']:
                for filename in glob.glob(pattern):
                    shutil.move(filename, './tooshort/')
            print("Skipped to tooshort")
    
    # Move files to appropriate directories
    for filename in glob.glob('*.fq'):
        shutil.move(filename, 'fq/')
    for filename in glob.glob('*.fa'):
        shutil.move(filename, 'fa/')
    
    # Combine all .si.fa files into one
    with open('all.seq.fa', 'w') as outfile:
        for filename in glob.glob('fa/*.si.fa'):
            with open(filename, 'r') as infile:
                shutil.copyfileobj(infile, outfile)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python _1-preprocess_barcodes.py <directory>")
        sys.exit(1)
    
    main(sys.argv[1])
