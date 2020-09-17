# SLRDash

## A simple webapp dashboard that helps with the multi-reviewer process of a Systematic Literature Review (SLR)

![Demo1](/SLRDash_demo1.png)
![Demo2](/SLRDash_demo2.png)

## Features:
- Easily review articles based on title, abstract and keywords
- Accomodates three independant reviewers
- Shows review history
- Allows reviewers to leave remarks/notes linked to reviews
- Allows to filter articles according to received review 
- Pop-up text field that keeps the personalised inclusion & exclusion criteria in the reviewers eyesight

### Setup:
1. Initialise all required python packages by using the `requirements.yml` file to create an identical, compatible anaconda environemnt with the following command: `conda env create --file requirements.yml` (potentially additional packages according to your target db have to be also installed.)
2. Change `settings.py` to own usage, specifically adapt the `database_dummy.txt` so that it points towards the database which holds your paper pool (from e.g. ScopusAPI). There are option for local or remote connections. Rename it `database.txt`.
3. Adapt the database structure according to the template defined in `models.py` or vis versa. Once defined any DMS can be used.
4. Assign descriptive reviewer names by searching for `name_placeholder_` in `app.html`
5. Webapp runs by default on *localhost:5000*, can be changed in `main.py` to own liking. If the service shall be available to the local network change `app.run()` to `app.run(host='0.0.0.0', port=5000)` in the `main.py` file (caution in exposing your webapp to untrusted networks!)