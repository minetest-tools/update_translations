# Minetest Update Translations

This Python script is intended for use with localized Minetest mods, i.e., mods that contain translatable strings of the form `S("This string can be translated")`. It extracts the strings from the mod's source code and updates the localization files accordingly. Minetest version 5.0.0 or later is required.

## Preparing your source code

This script makes assumptions about your source code. Before it is usable, you first have to prepare your source code accordingly.

### Choosing the translation domain name

You should always set translation domain name (for `minetest.get_translator`) to be identical to the mod name. The script currently does not support custom domain names. If you want to choose a different domain name regardless, the script is still usable, but you have to manually fix the output later (usually just the header of the `*.tr` files).

### Defining the helper functions

In any source code file with translatable strings, you have to manually define helper functions at the top with something like `local S = minetest.get_translator("<locale_domain>")`. Optionally, you can also define additional helper functions `FS`, `NS` and `NFS` if needed.

Here is the list of all recognized function names. All functions return a string.

* `S`: Returns translation of input. See Minetest's `lua_api.txt`. You should always have at least this function defined.
* `NS`: Returns the input. Useful to make a string visible to the script without actually translating it here.
* `FS`: Same as `S`, but returns a formspec-escaped version of the translation of the input. Supported for convenience.
* `NFS`: Returns a formspec-escaped version of the input, but not translated. Supported for convenience.

Here is the boilerplate code you have to add at the top of your source code file:

    local S = minetest.get_translator("<locale_domain>")
    local NS = function(s) return s end
    local FS = function(s) return minetest.formspec_escape(S(s)) end
    local NFS = function(s) return minetest.formspec_escape(s) end

Replace `<locale_domain>` above and optionally delete `NS`, `FS` and/or `NFS` if you don't need them.

### Preparing the strings

Enclose any translatable strings in a function of the form `S("Some string")`. For the string to be detected correctly, there must be exactly *one* uninterrupted string within the function; string concatenation, etc. is not allowed. If the thing between the function brackets is anything else (including a variable), it will be ignored by this script.

### A minimal example

This minimal code example sends "Hello world!" to all players, but translated according to each player's language:

    local S = minetest.get_translator("example")
    minetest.chat_send_all(S("Hello world!"))

### How to use `NS`

The reason why `NS` exists is for cases like this: Sometimes, you want to define a list of strings to they can be later output in a function. Like so:

    local fruit = { "Apple", "Orange", "Pear" }
    local function return_fruit(fruit_id)
       return fruit[fruit_id]
    end

If you want to translate the fruit names when `return_fruit` is run, but have the *untranslated* fruit names in the `fruit` table stored, this is where `NS` will help. It will show the script the string without Minetest translating it. The script could be made translatable like this:

    local fruit = { NS("Apple"), NS("Orange"), NS("Pear") }
    local function return_fruit(fruit_id)
       return S(fruit[fruit_id])
    end

## How to run the script

Place the script in the root directory of a mod and run it, and it will update the `template.txt` and any `*.tr` files present in that mod's `/locale` folder. If the `/locale` folder or `template.txt` file don't exist yet they will be created.

This script will also work in the root directory of a modpack. It will run on each mod inside the modpack in that situation.

It has the following command line options:

    i18n.py [OPTIONS] [PATHS...]

    --help, -h: prints this help message
    --recursive, -r: run on all subfolders of paths given
    --mods, -m: run on locally installed modules
    --no-old-file, -O: do not create *.old files
    --sort, -s: sort output strings alphabetically
    --break-long-lines, -b: add extra line-breaks before and after long strings
    --print-source, -p: add comments denoting the source file
    --verbose, -v: add output information
    --truncate-unused, -t: delete unused strings from files

The script will preserve any comments in an existing `template.txt` or the various `*.tr` files, associating them with the line that follows them. So for example:

    # This comment pertains to Some Text
    Some text=
    
    # Multi-line comments
    # are also supported
    Text as well=

Note that whenever the translation files are regenerated, the translation lines will be grouped by source `.lua` filename and sorted alphabetically, so don't bother manually organizing the order of the lines in the file yourself.

If the mod's source changes in such a way that a line with an existing translation or comment is no longer present, the unused line will be moved to the bottom of the translation file under the header:

    ##### not used anymore #####

This allows for old translations and comments to be reused with new lines where appropriate. This script doesn't attempt "fuzzy" matching of old strings to new, so even a single change of punctuation or spelling will put strings into the "not used anymore" section and require manual re-association with the new string.

## PO files conversion

This script will automatically convert `.po` files (from GNU gettext and the like)
if they exist in the `locale/` directory and a corresponding `.tr` file
*doesn't* exist. The .tr file that results will be reprocessed in
later runs so any "no longer used" strings will be preserved.
Note that "fuzzy" tags will be lost in this process.

## bash auto-completion

When running on Linux to install `bash_completion` for `i18n`, you can run

    mkdir -p ${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion/completions
    ln -s $PWD/bash-completion/completions/i18n ${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion/completions/i18n.py

This will provide bash auto-completion for this script (you have to run it without using `python3 i18n` command, use `./i18n.py` instead (or `i18n.py` if provided by `$PATH`)).
