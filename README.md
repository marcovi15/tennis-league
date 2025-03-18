# Leamington Tennis League

This repo was created to simplify and automate the process of signing up, matching up players, and keeping track of the rankings in a local Tennis league.
It uses a Google Sheets document as an interface, which could be used to create visualisations of players stats in the future.

## To run
First, set up a virtual environment
```commandline
python -m venv venv
venv/Scripts/activate
pip install -r requirements
```
If running from Linux, activate using `source venv/Bin/activate` instead.

Now you can run the code from your IDE of choice or from command window, by running ``python main.py``.


## To test
This project uses pytest, so just activate your virtual environment as described above and run ``pytest`` from command window.

## Docs
The existing docs were used to capture the rules of the league and not to document the code itself. 
If you'd like to contribute to the docs, you can do so by editing/adding the files inside ``docs``.
To regenerate the docs, you should just push the changes to GitHub, but you can regenerate them locally by running ``make html`` from command window.
