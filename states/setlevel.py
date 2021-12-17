import os, csv
asset_dir = os.path.join(os.getcwd(), "asset")


level = list()
with open(os.path.join(asset_dir, "lobby_level.csv"), "r") as readfile:
  level = csv.reader(readfile)

