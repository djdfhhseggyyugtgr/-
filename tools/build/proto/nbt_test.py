# Feasibility test: write a 1.21.1 structure .nbt (DataVersion 3955) with nbtlib, read back,
# write SNBT for git diffing, and check mcschematic/litemapy version support.
import sys, gzip, io
from nbtlib import File, Compound, List, Int, String, Double, serialize_tag, parse_nbt
out = sys.argv[1]
palette = [Compound({'Name': String('minecraft:air')}),
           Compound({'Name': String('minecraft:stone_bricks')}),
           Compound({'Name': String('minecraft:oak_stairs'), 'Properties': Compound({'facing': String('north'), 'half': String('bottom'), 'shape': String('straight'), 'waterlogged': String('false')})})]
blocks = []
W,H,L = 5,4,5
for x in range(W):
    for z in range(L):
        blocks.append(Compound({'pos': List[Int]([x,0,z]), 'state': Int(1)}))
blocks.append(Compound({'pos': List[Int]([2,1,0]), 'state': Int(2)}))
root = File({'DataVersion': Int(3955), 'size': List[Int]([W,H,L]), 'palette': List[Compound](palette),
             'blocks': List[Compound](blocks), 'entities': List[Compound]([])}, gzipped=True)
root.save(out)
f = File.load(out, gzipped=True)
print('DataVersion', int(f['DataVersion']), 'size', [int(v) for v in f['size']], 'blocks', len(f['blocks']), 'palette', len(f['palette']))
snbt = serialize_tag(f, indent=1)
print('SNBT lines', snbt.count('\n')+1)
back = parse_nbt(snbt)
print('SNBT roundtrip equal:', Compound(f) == back)
import mcschematic
names = [v.name for v in mcschematic.Version]
print('mcschematic has JE_1_21_1:', 'JE_1_21_1' in names, 'latest:', names[-3:])
import litemapy, inspect
print('litemapy Schematic defaults:', inspect.signature(litemapy.Schematic.__init__))
