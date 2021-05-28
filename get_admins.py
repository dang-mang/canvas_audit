import os
import subprocess
import pandas as pd
from config import *
from fix_json import *
from merge_csv import *
from concat_IDs import *
directory = "data/"
input_filename = directory + "input.json"
output_filename = directory + "output.csv"

def get_command(sys_id):
    #generate command with sys id
    return f"curl -H \"Authorization: Bearer {token}\" \"{URL[0]}{sys_id}{URL[1]}\" >> {input_filename}"

def get_IDs(): 
    #get data from source
    data = pd.read_csv(directory + "source.csv", header=0)
    sys_IDs = list(data['canvas_user_id'].to_list())
    num_users = len(sys_IDs) 
    print(f"Found {num_users} users in source.csv.\nPreparing to download data from {URL[0]}")
    return sys_IDs

def write_to_file(sys_IDs):
    if not os.path.exists(directory):
        os.makedirs(directory)

    os.system(f"echo \"[\" >> {input_filename}")
    num_users = len(sys_IDs) 
    for n in sys_IDs:
        os.system(get_command(n))
        if n != sys_IDs[-1]:
            os.system(f"echo \",\" >> {input_filename}")    
        percent = sys_IDs.index(n)/num_users * 100 
        print(f"Download progress - {round(percent,2)}% ({sys_IDs.index(n)}/{num_users})")
    os.system(f"echo \"]\" >> {input_filename}")
    input_string = input_filename.split("/")[1]

    print(f"Finished downloading {num_users} rows of user data.\nNow converting {input_string} to {output_filename}")

def clean_files():
    keep = "admins_final.csv"
    
    for filename in os.listdir(directory):
        if filename != keep:
            os.remove(os.path.join(directory + filename))

def main():
    sys_IDs = get_IDs()
    write_to_file(sys_IDs)
    print("Fixing JSON and converting to CSV...")
    fix_json(input_filename)
    print("CSV file created.\nMerging source file and output file...")
    merge_csv()
    print("CSV file merged.\nFetching IDs from API...")
    concat_IDs() 
    print("IDs fetched from API.\nMerging final CSV file...")
    merge_csv(source_filename = 'id.csv', output_filename = 'merged.csv', final = 'admins_final.csv', first = 'l_email' ,last = 'l_email')
    print("Final CSV file successfully generated. Cleaning files...")
    clean_files()
    print("Process complete.")

if __name__ == "__main__":
    # execute only if run as a script
    main()

