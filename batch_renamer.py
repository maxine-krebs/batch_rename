import os
import argparse
import re

def str2bool(v):
  if isinstance(v, bool):
    return v
  if v.lower() in ('yes', 'true', 't', 'y', '1'):
    return True
  elif v.lower() in ('no', 'false', 'f', 'n', '0'):
    return False
  else:
   raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.add_argument("directory")
parser.add_argument("-y", type=str2bool, nargs='?',
                      const=True, default=False,
                      help="skip the checks per rename")
args = parser.parse_args()

directory = args.directory

prog = re.compile("(^\S+)\.(S\d+e\d+)")

for file in os.listdir(directory):
  filename, file_extension = os.path.splitext(file)
  show_name = prog.search(filename).group(0)
  new_title = show_name + file_extension

  current_file = directory + file
  new_file = directory + new_title

  answer = ""
  if args.y == True:
    answer = "y"

  while answer not in ["y", "n", "q"]:
    print("re-naming file: {0} to: {1}".format(current_file, new_file))
    answer = input("👍? [(y)es/(n)o/(q)uit]").lower()

  if answer == "y":
    os.rename(current_file, new_file)
  elif answer == "q":
    print("Goodbye 👋")
    exit(0)
  else:
    continue


