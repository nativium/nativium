# Commands

Commands are functions executed from command line (terminal) that let you work with Nativium without need other tools or complex GUI.

Every command script in Nativium is a python file hosted on **commands** folder. 

Commands are simple functions that will receive command line arguments, the project path and that will executed desired operations. Example:

```python nativium.py clean```

or

```python nativium.py code format```

So, when you execute `python nativium.py clean` the Nativium system will search for a file called **clean.py** inside folder **commands** (commands/clean.py) and will send all parameters to a function inside it called **run**.

If you don't remember what commands are available, you can execute the **bootstrap** file to list all commands:

```python nativium.py```

If you want create your own commands put the file inside folder **commands** and execute `python nativium.py` on terminal to see it in command list.
