import sys


if len(sys.argv[1]) != 2:
    print("Invalid arguments.\nSyntax: python3 config.py path_to_your_file")
    exit(1)

with open("{}/filepath.txt", "w+") as file:
    file.write(sys.argv[1])

print("Configured {} as the path to your Api Key. You can run this command at any time to change this in the future."
      .format(sys.argv[1]))
exit(0)
