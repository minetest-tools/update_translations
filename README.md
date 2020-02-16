This Python script is intended for use with localized Minetest mods, ie, mods that contain translatable strings of the form ``S("This string can be translated")``.

Place it in the root directory of a mod and run it, and it will update the ``template.txt`` and any ``.tr`` files present in that mod's ``/locale`` folder.

This script will also work if you place it in the root directory of a modpack. It will run on each mod inside the modpack in that situation.