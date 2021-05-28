import os
import sys
def fix_json(input_filename, directory = "data/", output_filename = "output.csv"):
    output_path = directory + output_filename

    with open(input_filename) as f:
        newText=f.read().replace('}{', '},\n{').replace("]\n[",",").replace(",\n]","\n]")
    with open(input_filename, "w") as f:
        f.write(newText)
    
    os.system(f"python3 json_to_csv.py l {input_filename} {output_path}")

def main():
    print(sys.argv[1])
    fix_json(sys.argv[1])

if __name__ == "__main__":
    # execute only if run as a script
    main()

