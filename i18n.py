#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script to generate the template file and update the translation files.
#
# Copyright (C) 2019 Joachim Stolberg
# LGPLv2.1+
# 
# Copy the script into the mod root folder and run it there.

from __future__ import print_function
import os, fnmatch, re, shutil

#group 2 will be the string, groups 1 and 3 will be the delimiters (" or ')
#TODO: support [[]] delimiters
pattern_lua = re.compile(r'[ \.=^\t,]S\((["\'])((?:\\\1|(?:(?!\1)).)*)(\1)[ ,\)]', re.DOTALL)

pattern_tr = re.compile(r'(.+?[^@])=(.+)')
pattern_name = re.compile(r'^name[ ]*=[ ]*([^ ]*)')
pattern_tr_filename = re.compile(r'\.tr$')

#attempt to read the mod's name from the mod.conf file. Returns None on failure
def get_modname(folder):
    with open(folder + "mod.conf", "r", encoding='utf-8') as mod_conf:
        for line in mod_conf:
            match = pattern_name.match(line)
            if match:
                return match.group(1)
    return None

#If there are already .tr files in /locale, returns a list of their names
def get_existing_tr_files(folder):
    out = []
    for root, dirs, files in os.walk(folder + 'locale/'):
        for name in files:
            if pattern_tr_filename.search(name):
                out.append(name)
    return out

# Writes a template.txt file
def write_template(templ_file, lkeyStrings):
    lOut = []
    lkeyStrings.sort()
    for s in lkeyStrings:
        lOut.append("%s=" % s)
    with open(templ_file, "wt", encoding='utf-8') as template_file:
        template_file.write("\n".join(lOut))

# Gets all translatable strings from a lua file
def read_lua_file_strings(lua_file):
    lOut = []
    with open(lua_file, encoding='utf-8') as text_file:
        text = text_file.read()
        for s in pattern_lua.findall(text):
            s = s[1]
            s = re.sub(r'"\.\.\s+"', "", s)
            s = re.sub("@[^@=0-9]", "@@", s)
            s = s.replace("\n", "@n")
            s = s.replace("\\n", "@n")
            s = s.replace("=", "@=")
            lOut.append(s)
    return lOut

# Gets strings from an existing translation file
def import_tr_file(tr_file):
    dOut = {}
    if os.path.exists(tr_file):
        with open(tr_file, "r", encoding='utf-8') as existing_file :
            for line in existing_file.readlines():
                s = line.strip()
                if s == "" or s[0] == "#":
                     continue
                match = pattern_tr.match(s)
                if match:
                    dOut[match.group(1)] = match.group(2)
    return dOut

# Walks all lua files in the mod folder, collects translatable strings,
# and writes it to a template.txt file
def generate_template(folder):
    lOut = []
    for root, dirs, files in os.walk(folder):
        for name in files:
            if fnmatch.fnmatch(name, "*.lua"):
                fname = os.path.join(root, name)
                found = read_lua_file_strings(fname)
                print(fname, len(found))
                lOut.extend(found)
    lOut = list(set(lOut))
    lOut.sort()
    templ_file = folder + "locale/template.txt"
    write_template(templ_file, lOut)
    return lOut

# Updates an existing .tr file, copying the old one to a ".old" file
def update_tr_file(lNew, mod_name, tr_file):
    print("updating " + tr_file)
    lOut = ["# textdomain: %s\n" % mod_name]

    #TODO only make a .old if there are actual changes from the old file
    if os.path.exists(tr_file):
        shutil.copyfile(tr_file, tr_file+".old")

    dOld = import_tr_file(tr_file)
    for key in lNew:
        val = dOld.get(key, "")
        lOut.append("%s=%s" % (key, val))
    lOut.append("##### not used anymore #####")
    for key in dOld:
        if key not in lNew:
            lOut.append("%s=%s" % (key, dOld[key]))
    with open(tr_file, "w", encoding='utf-8') as new_tr_file:
        new_tr_file.write("\n".join(lOut))

# Updates translation files for the mod in the given folder
def update_mod(folder):
    modname = get_modname(folder)
    if modname is not None:
        print("Updating translations for " + modname)
        data = generate_template(folder)
        for tr_file in get_existing_tr_files(folder):
            update_tr_file(data, modname, folder + "locale/" + tr_file)
    else:
        print("Unable to find modname in folder " + folder)


update_mod("./")
print("Done.")
