fungitrack
==========

Databases assignment to create a database application


### Basic setup instructions ###

1. Setup [github](https://github.com/) and [git](https://help.github.com/articles/set-up-git).

2. Clone the [repo](https://github.com/kazagistar/fungitrack) with `git clone https://github.com/kazagistar/fungitrack.git`.

3. Install [Python](http://www.python.org/getit/) programming language.

4. Install [pip](http://www.pip-installer.org/en/latest/installing.html) (python's package manager).

5. Run `pip install -r requirements.txt` to install the requirements.

6. Run `python server.py`. It should track file changes and automatically reload changes in the server.

7. Navigate to the [webpage](http://localhost:5000)


#### Additional setup notes ####

- On windows, you might have to give the full path for the programs in the command line.

- Lab computers come preinstalled with git, python, and pip. However, since you don't have admin access for step 5, you will have to setup a [virtualenv](https://pypi.python.org/pypi/virtualenv) which is a bit involved.

- On OSX, the easiest way to install most dev stuff is by getting [homebrew](http://brew.sh/) which can be done by `ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"`. Update to newest python with pip included: `brew install python`. Install git: `brew install git`.

- If you want to push back to the repo, you will have to send me your github username so I can add you as a collaborator.


### Workflow ###

There are many possible workflows; git is a powertool and it is worth learning to use it effectively. However, here is a simple workflow that should allow you to get started quickly. 

Call these commands from inside the git repo. Alternatively, you a graphical option.

- `git commit -a` to add your most recent changes to a commit. This should open up. Alternatively, you can add specific files with `git add <filename>` and then commit the added changes with `git commit`. Note: these commits are local to your computer, not shared.

- `git pull`: Grabs the latest changes from the server. However, if you have made any local commits, you might conflict. To resolve this, you have to `git fetch` the changes, and then `git merge` them in, and then resolve differences in the files.

- `git push` to send your changes up to the server. If someone else pushed changes since you last pulled, you will have to fetch and merge as above before you can push.

- `git status` to see what the state of git is (what files have been added and modified, etc)