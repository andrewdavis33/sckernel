import argparse
import os

def configure():
  sckernel_dir = os.path.dirname(os.path.realpath(__file__))
  
  ap = argparse.ArgumentParser(description=
    "Create a configuration file for sckernel to successfully "
    "launch subproccesses for sclang and python"
  )
  ap.add_argument('-p', '--python', 
    help="Path to a version of Python 3.5 or higher.", default="python")
  ap.add_argument('-s', '--sclang', 
    help="Path to sclang binary.", default="sclang")
  args = ap.parse_args()
 
  with open(os.path.join(sckernel_dir, "paths.cfg"), "w") as w:
    w.write("python=" + args.python + "\n")
    w.write("sclang=" + args.sclang + "\n")

  print("Path configuration file written.")

if __name__ == '__main__':
  configure()
