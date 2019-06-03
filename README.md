Github Gists query
==================

This script queries github gists agains username

The script is using a file(last_check file) to store the last time it performed a query. Based on that it pull anything that comes up newer.

Configuration
------------

The script can be cofigured using environment variables.


* LAST_CHECK_FILE - absolute path to the last_check file
* GITHUB_USERNAME - the username to be queried


How to run
------------------

Run in virtual environment

```
# Get this repo and navigate to it
git clone https://github.com/man0v/github_gists.git && cd github_gists

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the script
./github_gists.py
```

Run in docker

```
# Get this repo and navigate to it
git clone https://github.com/man0v/github_gists.git && cd github_gists

# Build image
docker build . -t github_gists

# Run
docker run --rm github_gists

# In order to preserve the last_check file, run with a volume
docker run --rm -v /path/to/last_check:/app/last_check github_gists
```
