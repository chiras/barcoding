import os
import glob
import pandas as pd

def process_files(directory, output_file):
    files = glob.glob(os.path.join(directory, "*fm"))
    
    all_indices = set()
    file_data = {}

    # Read all files and collect indices
    for file in files:
        base_name = os.path.splitext(os.path.basename(file))[0]
        file_data[base_name] = {'indices': {}, 'columns': []}
        
        with open(file, 'r') as f:
            first_line = f.readline().strip()
            num_columns = len(first_line.split("\t"))
           
            if num_columns == 2:
                file_data[base_name]['columns'] = ['class']
            elif num_columns == 3:
                file_data[base_name]['columns'] = ['id', 'class']
            elif num_columns == 4:
                file_data[base_name]['columns'] = ['id', 'cov', 'class']
            else:
                print(f"Unexpected number of columns in file {file} ({num_columns}). Skipping.")
                continue

            # Read file content
            f.seek(0)  # Reset file pointer to beginning
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 2:  # Ensure we have at least the index and one value
                    index = parts[0]
                    values = parts[1:]
                    file_data[base_name]['indices'][index] = values
                    all_indices.add(index)
    
    all_indices = sorted(all_indices)  # Sort indices to maintain order

    # Prepare the header and data for output
    headers = ['ID']
    for name, file_info in file_data.items():
        for col in file_info['columns']:
            # Remove unwanted substrings from header names
            clean_name = name.replace("all.fa.", "").replace(".out", "")
            headers.append(f"{clean_name}.{col}")

    data = []

    for index in all_indices:
        row = [index]
        for file_name, file_info in file_data.items():
            values = file_info['indices'].get(index, ['NA'] * len(file_info['columns']))
            row.extend(values + ['NA'] * (len(file_info['columns']) - len(values)))
        data.append(row)

    # Create a DataFrame and write to file
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    directory = "."  # Current directory
    output_file = "combined_output.tsv"
    process_files(directory, output_file)
    print(f"Combined data written to {output_file}")
