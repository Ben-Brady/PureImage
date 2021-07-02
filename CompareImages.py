from Modules import ImageHash
import io
from pathlib import Path


def SelectFilefromDir(Dir: Path):
    while True:
        Files = list(Dir.iterdir())
        for x, file in enumerate(Files):
            print(f"{x}: {file}")
        Choice = input('Select:')
        try:
            Selection = Files[int(Choice)]
        except Exception:
            print('\n''Invalid Selection''\n')
        else:
            return Selection


Files = [io.BytesIO]*2
RootDir = 'Test/Images'
for x in range(2):
    print('\n'f"Select File {x+1}"'\n')
    Selection = Path(RootDir)
    while Selection.is_dir():
        Selection = SelectFilefromDir(Selection)

    Files[x] = Selection

for x, File in enumerate(Files):
    with open(File, 'rb') as fObj:
        Files[x] = ImageHash.Hash(fObj.read())

print(f"Distance: {ImageHash.Distance(Files[0],Files[1])}")
