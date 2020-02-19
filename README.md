This Python script is intended for use with localized Minetest mods, ie, mods that contain translatable strings of the form ``S("This string can be translated")``.

Place it in the root directory of a mod and run it, and it will update the ``template.txt`` and any ``.tr`` files present in that mod's ``/locale`` folder.

This script will also work if you place it in the root directory of a modpack. It will run on each mod inside the modpack in that situation.

It has the following command line options:

```
i18n.py [OPTIONS] [PATHS...]

--help, -h : prints this help message
--recursive, -r : run on all subfolders of paths given
--installed-mods : run on locally installed modules
--verbose, -v : add output information
```

The script will preserve any comments in the template.txt or the various .tr files, associating them with the line that follows them. So for example:

```
# This comment pertains to Some Text
Some text=

# Multi-line comments
# are also supported
Text as well=
```

Note that whenever the translation files are regenerated the translation lines will be grouped by source lua filename and sorted alphabetically.

If the mod's source changes in such a way that a line with an existing translation or comment is no longer present, the unused line will be moved to the bottom of the translation file under the header:

```
##### not used anymore #####
```
