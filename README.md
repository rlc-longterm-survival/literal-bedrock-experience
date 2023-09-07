# Literal Bedrock Experience

> Original author: [yezhiyi9670](https://github.com/yezhiyi9670)

This is a simple script for creating a Literal Bedrock Experience™ resource pack for Minecraft.

## Why did you make it

This started as a survival challenge where all textures become bedrock. We want to see if each member can still beat the game and how long we'd take.

## Usage

What you need to do is to put the folder original Minecraft resources into the `original` directory and change configs in the `mask` directory.

```plain
- original
  - 1.20.1 (arbitrary directory name)
    - assets
      + ...
- mask
  - bedrock.png (the bedrock texture)
  - modes-exception.json (config)
  - pack.mcmeta (info for generated pack)
+ overrides (override files)
+ output (output files)
+ dist (generated zip files)
```

Then run `transformer.py`. Output will be found in `output` and `dist` directory.
