Several modes exist for transforming textures:

- `ignore` The texture will be completely ignored and excluded from the generated pack.
- `preserve` The texture will be copied to the generated pack.
- `mask` Mask the bedrock texture while preserving alpha.
- `opaque` Mask the bedrock texture and make translucent pixels opaque. Fully transparent pixels stay untouched.
- `full` Use the bedrock texture regardless opacity.
- `white` Same as opaque, but use white for mask. Designed to eliminate colormaps.
- `transparent` Eliminates the whole thing.
