#!/usr/bin/env python
from pathlib import Path
from sys import stderr, argv
from configparser import ConfigParser
from os import chdir
from shutil import copy

def eprint(*arg, **kwarg):
    if "key" in kwarg:
      kwarg.pop("file")
    print(*arg, file=stderr, **kwarg)

def ff_inst_err(reason):
    eprint(f"firefox installation invalid: {reason}")
    exit(1)

CONFIGS = """toolkit.legacyUserProfileCustomizations.stylesheets
layers.acceleration.force-enabled
gfx.webrender.all
gfx.webrender.enabled
layout.css.backdrop-filter.enabled
svg.context-properties.content.enabled
widget.gtk.ignore-bogus-leave-notify = 1"""

if __name__ == "__main__":
  chdir(str(Path(argv[0]).absolute().parent))
  
  ff = Path("~/.mozilla/firefox").expanduser()
  if not ff.exists():
    ff_inst_err("~/.mozilla/firefox doesn't exists")
  
  cfg = ConfigParser()
  cfg.read(ff / "profiles.ini")
  profiles = []
  default = None
  for k in cfg.keys():
    if k.startswith("Install"):
      default = cfg[k]["Default"]
    if k.startswith("Profile"):
      profiles.append(cfg[k]["Path"])
  if default is None or default not in profiles:
    ff_inst_err("no Installations found is profiles.ini")

  print("Select firefox profile (marked one is the default):")
  for n, p in enumerate(profiles):
    print(f"  {n:2d}. {p}{' **' if p == default else ''}")
  ind_def = profiles.index(default)
  while True:
    inp = input(f"Selection? (0-{len(profiles)}) [{ind_def}] ")
    if inp == "":
        inp = ind_def
        break
    try:
      inp = int(inp)
      if 0 <= inp < len(profiles):
        break
      else:
        raise ValueError
    except ValueError:
      print(f"Invalid: {inp}")

  selected = profiles[inp]
  path = ff / selected / "chrome"
  path.mkdir(exist_ok=True)
  copy(Path("userChrome.css"), path)

  print("Please now go to about:config and change the following to true:")
  for l in CONFIGS.splitlines():
    print(l)
    input("Next? ")
  
  print("Now go to Sidebery Settings -> Styles Editor -> Tabs, and set \"Inner Gap\" to 8px")
  input("Done? ")

  print("Now go to Sidebery Settings -> Settings -> General, and turn on \"Add preface to browser window's title if Sidebery sidebar is active\"")
  input("Done? ")

