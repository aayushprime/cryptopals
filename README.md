# cryptopals
My attempt at cryptopals
1. Clone the repository
1. Set PYTHONPATH="root repository folder"
1 . And to run go inside with `python3 filename.py` from the folder the file is in.

All this is easier is vscode use following config
open repository home with vscode
use config .vscode/launch.json, with setting run from file folder
```{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd":"${fileDirname}",
            "env": {
                "PYTHONPATH":"${workspaceFolder}"
            }
        }
    ]
}```
