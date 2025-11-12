# zipapp-creator

A simple tool to create a zipapp for your Python project.

## Features

- A simple yet easy-to-use GUI

- Automatic install the dependencies and package them into the output zipapp

- Implement an approach to create a so-called "self-extracting" zipapp, which 
solves the following problems:
  - Add a workaround to make your zipapp work with c extensions, which considered 
  unsupported in official documentation.
  
  > See [zipapp#Caveats](https://docs.python)
  > 
  > If your application depends on a package that includes a C extension, 
  > that package cannot be run from a zip file (this is an OS limitation, 
  > as executable code must be present in the filesystem for the OS loader 
  > to load it). In this case, you can exclude that dependency from the 
  > zipfile, and either require your users to have it installed, or ship
  > it alongside your zipfile and add code to your __main__.py to include
  > the directory containing the unzipped module in sys.path. In this case,
  > you will need to make sure to ship appropriate binaries for your target
  > architecture(s) (and potentially pick the correct version to add to 
  > sys.path at runtime, based on the user’s machine).
  
  - Make it is easy to access the assets files inside the package using regular 
  apis, such as  `importlib.resources` or `pkgutil.resource_filename`.

- Create a startup script of the output zipapp on Windows os.

