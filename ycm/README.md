YCM config file
--------------------

### TLDR;

Copy the `.ycm_extra_conf.py` file at the root of your project and adjust the
flags as needed.

The `ycm` `vim` plugin expects, given a file name, to be fed a list of compiler
flags for it. This is then used for static analysis and in-editor warnings and
diagnostic messages. You can use a global such configuration file and specify the
path to it from within the `.vimrc`, but the flags for one project may not
necessarily be appropriate from another. It's therefore recommended/expected for
each project to have its own '.ycm_extra_conf.py'.
FMI see [here](https://github.com/ycm-core/YouCompleteMe).

This file I've uploaded here _must_ be copied to the root of a given project.
It contains some functions that will traverse each subdirectory to figure out
flags and whatnot. This means putting it e.g. in your home directory for global
use will not only not work as intended, but it will end up trying to traverse
most of the file system recursively!
Again: **copy this file into the ROOT directory of your project**.



