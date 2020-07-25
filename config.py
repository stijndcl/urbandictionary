import sys


if len(sys.argv) != 2:
    print("Invalid arguments.\nSyntax: python3 config.py path_to_your_file")
    exit(1)

with open("{}/filepath.txt".format(sys.path[0]), "w+") as file:
    file.write(sys.argv[1])

print("Configured {} as the path to your API Key.\nYou can run this command at any time to change this in the future."
      .format(sys.argv[1]))
exit(0)
