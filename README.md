# ProjectMimir
============

Tool for archiving Files. Fully written in Python

The gaol of this project is, to create a tool, that can archive basically everything. By writing it in python and using as few external stuff (SQL etc.) as possible, the compability should be maximized.

For improveing usability a shellscript can be placed at ~/bin, that start mimir with the database location as argument:
    #!/bin/bash
    python path/to/ProjectMimir/consolfrontend.py $1
