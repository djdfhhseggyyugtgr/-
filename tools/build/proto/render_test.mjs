// Feasibility test: headless CPU render of a 1.21.1 structure .nbt with deepslate + headless-gl (Xvfb/Mesa).
// usage: node render_test.mjs <node_modules dir> <assets dir> <in.nbt> <out.png> [yawDeg]
import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
const [nm, assets, inNbt, outPng, yawArg] = process.argv.slice(2)
const req = createRequire(path.join(nm, 'x.js'))
const createGL = req('gl')
const { PNG } = req('pngjs')
const ds = await import(path.join(nm, 'deepslate/lib/index.js'))
const { mat4 } = await import(path.join(nm, 'gl-matrix/esm/index.js'))
const { BlockDefinition, BlockModel, Identifier, TextureAtlas, Structure, StructureRenderer, NbtFile } = ds
const J = f => JSON.parse(fs.readFileSync(path.join(assets, f), 'utf8'))
const blockstates = J('summary_assets_block_definition_data.min.json')
const models = J('summary_assets_model_data.min.json')
const uvMap = J('atlas_all_data.min.json')
const atlasPng = PNG.sync.read(fs.readFileSync(path.join(assets, 'atlas_all_atlas.png')))
const blockDefinitions = {}, blockModels = {}
for (const id of Object.keys(blockstates)) blockDefinitions['minecraft:' + id] = BlockDefinition.fromJson(blockstates[id])
for (const id of Object.keys(models)) blockModels['minecraft:' + id] = BlockModel.fromJson(models[id])
for (const m of Object.values(blockModels)) m.flatten({ getBlockModel: id => blockModels[id.toString()] })
const size = 2 ** Math.ceil(Math.log2(Math.max(atlasPng.width, atlasPng.height)))
const idMap = {}
for (const id of Object.keys(uvMap)) {
  const [u, v, du, dv] = uvMap[id]
  const dv2 = (du !== dv && id.startsWith('block/')) ? du : dv
  idMap[Identifier.create(id).toString()] = [u / size, v / size, (u + du) / size, (v + dv2) / size]
}
const pot = n => 2 ** Math.ceil(Math.log2(n))
const S = pot(Math.max(atlasPng.width, atlasPng.height))
const padded = new Uint8Array(S * S * 4)
for (let y = 0; y < atlasPng.height; y++) padded.set(atlasPng.data.subarray(y * atlasPng.width * 4, (y + 1) * atlasPng.width * 4), y * S * 4)
const img = { width: S, height: S, data: padded }
const atlas = new TextureAtlas(img, idMap)
const resources = {
  getBlockDefinition: id => blockDefinitions[id.toString()],
  getBlockModel: id => blockModels[id.toString()],
  getTextureUV: id => atlas.getTextureUV(id),
  getTextureAtlas: () => atlas.getTextureAtlas(),
  getBlockFlags: id => ({ opaque: !/glass|leaves|stairs|slab|air/.test(id.toString()) }),
  getBlockProperties: () => null,
  getDefaultBlockProperties: () => null,
}
const structure = Structure.fromNbt(NbtFile.read(new Uint8Array(fs.readFileSync(inNbt))).root)
const [sx, sy, sz] = structure.getSize()
const W = 1024, H = 768
const gl = createGL(W, H, { preserveDrawingBuffer: true, antialias: false })
Object.defineProperty(gl, 'canvas', { value: { clientWidth: W, clientHeight: H, width: W, height: H }, configurable: true })
const renderer = new StructureRenderer(gl, structure, resources)
renderer.setViewport(0, 0, W, H)
const view = mat4.create()
const dist = Math.max(sx, sy, sz) * 1.8 + 4
mat4.translate(view, view, [0, 0, -dist])
mat4.rotateX(view, view, 30 * Math.PI / 180)
mat4.rotateY(view, view, (Number(yawArg ?? 45)) * Math.PI / 180)
mat4.translate(view, view, [-sx / 2, -sy / 2, -sz / 2])
gl.clearColor(0.85, 0.87, 0.9, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)
renderer.drawStructure(view)
const px = new Uint8Array(W * H * 4)
gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px)
const png = new PNG({ width: W, height: H })
for (let y = 0; y < H; y++) png.data.set(px.subarray((H - 1 - y) * W * 4, (H - y) * W * 4), y * W * 4)
fs.writeFileSync(outPng, PNG.sync.write(png))
let nonBg = 0; for (let i = 0; i < px.length; i += 4) if (Math.abs(px[i] - 217) > 8) nonBg++
console.log('rendered', outPng, `${W}x${H}`, 'size', [sx, sy, sz], 'non-background px', nonBg)
