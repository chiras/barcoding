import os
import subprocess
import argparse

def run_blast_local_nt(input_file, db, output_file, log_file):
    # Set the BLASTDB environment variable
    env = os.environ.copy()
    env['BLASTDB'] = "/LETHE/Members/data/Refs/NCBI/"
    
    command = [
        'blastn', '-query', input_file, '-db', 'nt', '-max_target_seqs', '1', '-perc_identity', '90', '-num_threads', '35',
        '-outfmt', '6 qseqid pident qlen length sseqid staxid ssciname'
    ]
    with open(output_file, 'w') as out, open(log_file, 'a') as log:
        return subprocess.Popen(command, stdout=out, stderr=log, env=env)

def run_blast_local(input_file, db, output_file, log_file):
    command = [
        'blastn', '-query', input_file, '-subject', db, '-max_target_seqs', '1', '-perc_identity', '90',
        '-outfmt', '6 qseqid pident qlen length sseqid'
    ]
    with open(output_file, 'w') as out, open(log_file, 'a') as log:
        return subprocess.Popen(command, stdout=out, stderr=log)

def run_blast_remote(input_file, output_file, log_file):
    command = [
        'blastn', '-query', input_file, '-remote', '-db', 'nt', '-max_target_seqs', '1', '-perc_identity', '90',
        '-outfmt', '"6 qseqid pident qlen length sseqid staxid ssciname"', '>', output_file, '2>>', log_file
    ]
    return subprocess.Popen(' '.join(command), shell=True)

def run_vsearch_direct(input_file, db, output_file, log_file):
    command = [
        'vsearch', '--usearch_global', input_file, '--db', db, '--id', '0.90', '--threads', '5',
        '--uc', output_file, '2>>', log_file
    ]
    return subprocess.Popen(' '.join(command), shell=True)

def run_vsearch_sintax(input_file, db, output_file, log_file):
    command = [
        'vsearch', '--sintax', input_file, '--db', db, '--tabbedout', output_file,
        '--strand', 'plus', '--sintax_cutoff', '0.9', '--threads', '5', '2>>', log_file
    ]
    return subprocess.Popen(' '.join(command), shell=True)

def main():
    parser = argparse.ArgumentParser(description="Classify sequences using various algorithms and databases.")
    parser.add_argument('input_file', type=str, help="Input FASTA file")
    args = parser.parse_args()

    input_file = args.input_file

    # Directories and databases
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    DBsebas = "/LETHE/Alex/tmp/EcuadorPlants/Ecuador_Sebastian_Plants_all.fa"
    DBviri = "/LETHE/Members/MB/_DBs/its2.global.2023-01-17.curated.tax.mc.add.fa"

    # Running classifications in parallel
    processes = [
        run_vsearch_direct(input_file, DBviri, "all.fa.vsearch-viri.out", os.path.join(log_dir, "vsearch-viri.log")),
        run_vsearch_direct(input_file, DBsebas, "all.fa.vsearch-sebas.out", os.path.join(log_dir, "vsearch-sebas.log")),
        run_vsearch_sintax(input_file, DBviri, "all.fa.vsearch-sintax.out", os.path.join(log_dir, "vsearch-sintax.log")),
        run_blast_local(input_file, DBviri, "all.fa.blast-viri.out", os.path.join(log_dir, "blast-viri.log")),
        run_blast_local(input_file, DBsebas, "all.fa.blast-sebas.out", os.path.join(log_dir, "blast-sebas.log")),
        run_blast_remote(input_file, "all.fa.blast-remote.out", os.path.join(log_dir, "blast-remote.log"))#,
        #run_blast_local_nt(input_file, "nt", "all.fa.blast-gb.out", os.path.join(log_dir, "blast-gb.log"))
]

    # Wait for each process to complete
    for i, process in enumerate(processes):
        process_name = f"Process {i+1} ({process.args[0]})"
        process.wait()
        print(f"{process_name} finished.")

if __name__ == "__main__":
    main()
