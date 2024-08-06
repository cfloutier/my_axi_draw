# my_axi_draw
a tool using axi draw api used to pilot my tracer

# installation

WIP

* install python
* install the axidraw python api : https://axidraw.com/doc/py_api 
  * download the package and unzip in a local folder named [AXIDRAW_FOLDER]
  * follow the installation.txt

```powershell
  # in this folder. creates the local virtual env in the venv folder (ignored in git)
  python -m venv venv
  # Activate the environment:

  #source ./venv/bin/activate # bash/zsh shells, like on mac, ubuntu
  .\venv\Scripts\Activate.ps1 # windows powershell

  # go to the api folder 
  cd [AXIDRAW_FOLDER]

  # install dependencies
  pip install . 
```

Note in vscode, I've added this settings because the path to axidraw was not found

in `.vscode\settings.json` :

```json
{

    "python.analysis.extraPaths": ["C:\\dev\\__tracer\\api\\AxiDraw_API\\AxiDraw_API_396"]
}
```






