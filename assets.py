import pathlib as pb

absPath = pb.Path.cwd()

# Assets path
assets = pb.Path(absPath/'assets')

# Game icon
gameIcon = pb.Path(assets/'icons/icon.png')

# Snake parts
rightHeadPart = pb.Path(assets/'parts/face-1.png')
upHeadPart = pb.Path(assets/'parts/face-2.png')
leftHeadPart = pb.Path(assets/'parts/face-3.png')
downHeadPart = pb.Path(assets/'parts/face-4.png')

straightHor = pb.Path(assets/'parts/straight-1.png')
straightVer = pb.Path(assets/'parts/straight-2.png')

turns = [] 
for i in range(0,4):
    turns.append(pb.Path(assets/f'parts/turn-{i+1}.png'))


invisible = pb.Path(assets/'parts/invisible.png')