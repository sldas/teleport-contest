# Initialization contract — source inspected during bootstrap

Source pin: NetHack 16ff59115315917b93185d026aeefea06db9b0f4, src/allmain.c newgame(), src/dungeon.c init_dungeons(). This is an initial source-reading contract, not a compiled-oracle proof. Organizer patches were subsequently applied during the successful native build; src/allmain.c was unchanged by that patch series. Broader patch effects still require function-level review.

The upstream startup sequence is:

1. Disable monster notices; initialize context and monster vital flags.
2. init_objects() before role_init().
3. role_init() before init_dungeons(), character initialization and artifacts.
4. init_dungeons() before initial inventory to establish monster generation context.
5. init_artifacts(), u_init_misc(), l_nhcore_init(), reset_glyphmap().
6. mklev(), u_on_upstairs(), vision_reset(), check_special_room().
7. Relocate a monster at the hero position if needed; makedog().
8. u_init_inventory_attrs(), initial display, optional reroll loop.
9. u_init_skills_discoveries(), optional wizard kit and legacy message.
10. Initialize realtime/save state; welcome(); enable monster notices.

Lua is an ordinary startup dependency: dungeon.c init_dungeons() initializes a private Lua state and loads dungeon.lua. allmain.c also initializes long-lived nhcore state. It cannot be deferred on the assumption that it only serves rare special levels.

The starter js/allmain.js currently hardcodes a seed8000 branch, player attributes and role, and calls fastforward functions around level generation and turn processing. This prevents its apparent RNG alignment from establishing general implementation coverage. Replace these paths at their actual dependency boundaries; do not add additional recorded-seed cases.

Next engineering slice: calibrate the patched C build, then inventory the state and effects of init_objects()/role_init()/init_dungeons() while establishing numeric and input contracts. Character inventory initialization occurs after level generation in this upstream version: do not import an older NetHack startup order from memory.
