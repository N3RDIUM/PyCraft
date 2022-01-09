import os
from logging import *
basicConfig(level=WARNING)

def warn(msg):
    warning(msg)

name = input('Enter name of block: ')
textures = []
texture_type = input('Enter texture type (One of all, topbottomsides, uniquetopbottomsides, unique): ')
if texture_type == "all":
    side = input('Enter texture for all sides: ')
    for i in range(6):
        textures.append(side)
elif texture_type == "topbottomsides":
    top_bottom = input('Enter texture for top and bottom: ')
    side = input('Enter texture for sides: ')
    textures.append(top_bottom)
    for i in range(4):
        textures.append(side)
    textures.append(top_bottom)
elif texture_type == "uniquetopbottomsides":
    top = input('Enter texture for top: ')
    bottom = input('Enter texture for bottom: ')
    side = input('Enter texture for sides: ')
    textures.append(top)
    for i in range(4):
        textures.append(side)
    textures.append(bottom)
elif texture_type == "unique":
    print('(0 = top, 1 = front, 2 = back, 3 = left, 4 = right, 5 = bottom)')
    for i in range(6):
        textures.append(input('Enter texture for side ' + str(i) + ': '))
else:
    print('Invalid texture type')
    exit()

# Check if textures exist
for i in textures:
    if not os.path.exists(f'../assets/textures/block/{i}.png'):
        warn(f'Texture {i} does not exist')

gen_code = f'''
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        {name}
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("{name}", *args, **kwargs)

        self.texture = {{
            "top": self.parent.textures["{textures[0]}"],
            "front": self.parent.textures["{textures[1]}"],
            "back": self.parent.textures["{textures[2]}"],
            "left": self.parent.textures["{textures[3]}"],
            "right": self.parent.textures["{textures[4]}"],
            "bottom": self.parent.textures["{textures[5]}"]
        }}
'''

# Save the file
if not os.path.exists(f'../Classes/terrain/blocks/{name}.py'):
    with open(f'../Classes/terrain/blocks/{name}.py', 'w') as file:
        file.write(gen_code)
else:
    print(f'{name}.py already exists!')
    exit()

print('BLOCK ADDITION SUCCESSFUL')
