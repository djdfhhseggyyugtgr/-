# Generate a larger test structure (a crude ruined arcade/sewer hall) to time headless rendering.
import sys, random
from nbtlib import File, Compound, List, Int, String
random.seed(1)
out=sys.argv[1]; W,H,L=64,24,64
pal=['minecraft:air','minecraft:stone_bricks','minecraft:cracked_stone_bricks','minecraft:mossy_stone_bricks','minecraft:deepslate_tiles','minecraft:water','minecraft:iron_bars','minecraft:lantern']
P={n:i for i,n in enumerate(pal)}
blocks={}
def put(x,y,z,n): blocks[(x,y,z)]=P[n]
for x in range(W):
  for z in range(L):
    put(x,0,z,'minecraft:deepslate_tiles')
    if 26<=x<=37: put(x,0,z,'minecraft:water')
for z in range(0,L,8):
  for x in (8,24,40,56):
    for y in range(1,14):
      put(x,y,z, random.choice(['minecraft:stone_bricks']*5+['minecraft:cracked_stone_bricks','minecraft:mossy_stone_bricks']))
for z in range(L):
  for x in range(W):
    if random.random()<0.85: put(x,14,z, random.choice(['minecraft:stone_bricks']*4+['minecraft:cracked_stone_bricks','minecraft:mossy_stone_bricks']))
for z in range(0,L,16): put(32,13,z,'minecraft:lantern')
for z in range(L):
  for y in range(1,4): put(25,y,z,'minecraft:iron_bars') if z%2 else None
bl=[Compound({'pos':List[Int]([x,y,z]),'state':Int(s)}) for (x,y,z),s in blocks.items()]
File({'DataVersion':Int(3955),'size':List[Int]([W,H,L]),'palette':List[Compound]([Compound({'Name':String(n)}) for n in pal]),'blocks':List[Compound](bl),'entities':List[Compound]([])},gzipped=True).save(out)
print('blocks',len(bl))
