
# Can print the path the file is in.  Works in jupyter notebooks, etc.
# Seems to be "recommended" way?  I assume platform neutral, etc.
from pathlib import Path
print(Path().absolute())





