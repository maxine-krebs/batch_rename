import os
import argparse
import re
from pathlib import Path

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("directory")
  parser.add_argument("type", choices=["movies", "shows"])
  parser.add_argument("-y", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="skip the checks per rename")
  parser.add_argument("--dry-run", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="dont actually write filename changes")
  parser.add_argument("-v", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="verbose output")

  args = parser.parse_args()
  skip_confirm = args.y
  dry_run = args.dry_run
  directory = args.directory
  type = args.type
  verbose = args.v

  if type == "shows":
    rename_matching("(^\S+)\.(s\d+e\d+)", directory, skip_confirm, dry_run, verbose)
  elif type == "movies":
    rename_matching("([\[a-zA-Z\]\.?]+)\.(\d+)", directory, skip_confirm, dry_run, verbose)

  print("done! 🎉")

def rename_matching(pattern, directory, skip_confirm=False, dry_run=False, verbose=False):
  prog = re.compile(pattern, flags=re.I)
  files = sorted(Path(directory).rglob('*.[ms][kpr][v4t]'))

  for file in files:
    current_file = str(file)
    filename, file_extension = os.path.splitext(file)
    matches = prog.search(filename)

    if matches == None:
      if verbose == True:
        print("no matches found in filename: {0}".format(current_file))
      continue

    show_name = matches.group(0)
    new_title = show_name + file_extension

    new_file = directory + new_title

    if current_file == new_file:
      if verbose == True:
        print("skipping: {0}".format(current_file, new_file))
      continue
    elif dry_run == True:
      print("{0} to: {1}".format(current_file, new_file))
    else:
      answer = ""

      if skip_confirm == True:
        answer = "y"

      while answer not in ["y", "n", "q"]:
        print("re-naming file: {0} to: {1}".format(current_file, new_file))
        answer = input("👍? [(y)es/(n)o/(q)uit]").lower()

      if answer == "y":
        os.rename(current_file, new_file)
        continue
      elif answer == "q":
        print("Goodbye 👋")
        exit(0)
      else:
        continue

def str2bool(v):
  if isinstance(v, bool):
    return v
  if v.lower() in ('yes', 'true', 't', 'y', '1'):
    return True
  elif v.lower() in ('no', 'false', 'f', 'n', '0'):
    return False
  else:
   raise argparse.ArgumentTypeError('Boolean value expected.')

main()
