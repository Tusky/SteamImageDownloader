# SteamImageDownloader
Downloads library/portrait and header images for given steam ids.

# Usage
To download images for HL and HL2 for example:
1.  `pipenv shell`
2. `python download.py 70 220`

# Note
To not hit the Steam API constantly it's cached for 24 hours. Every 24 hours, or when the data.json file is removed it will update the local DB.
