# Manual Minecraft Plugin Jars

Use this folder to store plugin jars that should be copied directly to the server
without relying on the container startup downloader.

## How to use

1. Place jar files in this directory.
2. Set `minecraft_manual_plugin_seed_enabled: true` in host vars.
3. Add jar filenames to `minecraft_manual_plugin_jars`.
4. Run the deploy playbook.

The deploy playbook will copy each listed jar to:

- `/srv/minecraft/data/plugins/<jar-name>`

This is useful as a fallback when upstream plugin URLs are unavailable.
