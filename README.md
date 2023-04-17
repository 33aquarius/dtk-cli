# Developer Toolkit (DTK) Command Line Interface
## Public Release Ver. 1.0

###### This code was written by 33aquarius (github.com/33aquarius). Feel free to use this public version for free and incorporate your own scripting (and if you're feeling extra generous, I wouldn't mind having it shared either :p). It would mean a lot to me if my software was able to help somebody maximize their productivity!


## Dependencies

Bare-minimum functionality for the interface requires installation of the following dependencies:

```
$ pip install numpy
$ pip install pandas
$ pip install matplotlib
$ pip install seaborn
$ pip install shutil
$ pip install statsmodels
$ pip install nltk
```

For the full range of functionalities offered within DTK-CLI's Public Release Ver. 1.0, the following dependencies are also required:

```
$ pip install statsmodels
$ pip install redshift-connector
$ pip install scikit-learn
$ pip install ta
$ pip install backtesting
$ pip install
$
$
```

## Starting up the CLI

This folder contains an interface for easily referencing code for use in future projects. A command line interface is provided which can be accessed via command terminal. The first call boots up the interface using its default settings (these can be personalized to each client), ad the second call does the same thing while showcasing every possible input argument that can be passed through DTK.py. Successfully running the file should automatically start the CLI in the terminal window.

```
$ DTK-CLI.py
$ DTK-CLI.py --f filepath --d df_cache_len_limit --tw terminal width
```

The second method of calling uses the argparse module to also allow for a few different inputs, if specifications beyond default presets are desired. They are, in order of appearance in the below example:

1. --fp filepath

2. --dl df_cache_len_limit

3. --tw terminal width

Successfully running the file should automatically start the CLI in the terminal window.

## CLI Help Screen




## Known Bugs, Issues

For Windows users, it may prove challenging to operate the interface while utilizing a Windows Subsystem for Linux (WSL) without modifying the code to remove discrepancies between how operating systems handle path addresses. The directories and the navigation of the files within them may have to be altered in code for any of the interface to be operational. My best suggestions for this are either moving this interface's source folder into WSL and running the CLI on Linux, or just sticking purely to Windows as the interface should never contain parts complex enough to yield considerable differences in performance based on the OS.
