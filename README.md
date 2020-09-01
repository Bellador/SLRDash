# SLRDash

## A simple webapp dashboard that helps with the multi-reviewer process of a Systematic Literature Review (SLR)

![Demo1](/SLRDash_demo1.png)
![Demo2](/SLRDash_demo2.png)

## Features:
- Easily review papers based on title, abstract and keywords
- Simple overview of the review history
- Filter for papers with specific reviews 
- Stores who performed the review on a given paper
- Pop-up text field that keeps the personalised inclusion & exclusion criteria for the given SLR in the reviwers eyesight

### Setup:
1. Initialise all required python packages by using the requirements.txt file to create an identical, compatible anaconda environemnt with the following command: `conda create --name myenv --file requirements.txt` (potentially additional packages according to your target db have to be also installed.)
2. Adapt the `database_dummy.txt` so that it points towards the database where your inital paper pool (from e.g. ScopusAPI) is located (local or remote) and rename it `database.txt`.
3. Adapt the database structure according to the template defined in `models.py` or vis versa. Ones defined any DMS can be used.
4. Webapp runs by default on *localhost:5000*, can be changed in `main.py` to own liking.