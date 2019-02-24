# ./libraries/app_bundle/FQL.py
This file contains all the logic needed t handle FlameZip (.fz)
-----------------------------
# Variables

# Functions
`byteify`
Workaround for converting str to bytes due to Encoding issues with using bytes()
`FMap`
This function converts a string like "0010010001" to a list [00,10,01,00,01]
`FlameZipArchive.__init__`
Creates string which archive contents will be stored
`FlameZipArchive.archiveFile`
Hash file and return contents
`FlameZipArchive.archiveDir`
Archive all files in a dir and all sub-directories
# Classes
`FlameZipArchive`
Class for creating .fz archives