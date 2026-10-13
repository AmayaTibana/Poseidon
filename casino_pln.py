ear Pipeline process

# Extract process
def extract_code():
    with open('casino.py', 'r') as file:
        code = file.read()
    return code

# Transform process
def transform_code(code):
    return code.replace('main()fds --- IGNORE ---', 'main()')

# Read process
def read_code():
    with open('casino.py', 'r') as file:
        updated_code = file.read()
    return updated_code

#spark or Dag

def main():
    number = int(input("Enter the number of games to play: "))
    play_multiple_games(number)

# Removed duplicate function definitions

def read_code():
    with open('casino.py', 'r') as file:
        updated_code = file.read()
# Build pipeline process with DAGs
dag = {
    'extract': lambda: extract_code(),
    'transform': lambda: transform_code(dag['extract']()),
    'read': lambda: read_code()
}

# Execute the pipeline
if __name__ == "__main__":
    updated_code = dag['read']()
    print(updated_code) 

#making a dag for the pipeline process 

# another try  

def another_try():
    updated_code = dag['read']()
    print(updated_code)