# Minecraft Client Mod Recommendations

Purpose: document optional player-side mods that work well with the Paper
server deployment in this repo without confusing them with server plugins.

## Recommended Minimap Stack

- Xaero's Minimap for an in-game minimap overlay.
- Xaero's World Map for a larger fullscreen map that complements the minimap.

These are client-side mods. They must be installed by each player in their own
Minecraft client and are not deployed through Ansible, Paper plugin lists, or
the server `mods` directory on hosts like `media1` and `media2`.

## Server Compatibility Notes

- The production servers in this repo run Paper, not Fabric or Forge.
- Do not add Xaero jars to `minecraft_paper_plugins`; they are not Bukkit or
  Paper plugins.
- Do not treat these as required for gameplay. Players without them should
  still be able to join normally.

## Server-Side Map Option

If a shared server-hosted map is needed, use BlueMap. BlueMap is the Paper-side
map service already supported by the deploy automation and can be exposed on a
dedicated web port for browser access.