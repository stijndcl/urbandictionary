import sys


if len(sys.argv[1]) != 2:
    print("Invalid arguments.\nSyntax: python3 config.py path_to_your_file")

with open("{}/filepath.txt", "w+") as file:
    file.write(sys.argv[1])
