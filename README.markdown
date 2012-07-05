=============
R-Play Client
=============


Alpha Setup
* Register http://young-sky-3165.herokuapp.com/players/register/ (HTTP plain text for the API and registration, use a new password)
* Put client.py anywhere -- Make a .rplay_profile with the following fields:

    export RPLAY_USERNAME=issackelly
    export RPLAY_PASSWORD=derpderpderp
    export RPLAY_DIR=/Users/*/Library/Application Support/Blizzard/StarCraft II/Accounts/*/*/Replays/Multiplayer


* Upload your existing replays:

    source .rplay_profile
    ./client.py /Users/*/Library/Application Support/Blizzard/StarCraft II/Accounts/*/*/Replays/Multiplayer/*

When you're going to play, turn on the auto-uploader:

    source .rplay_profile
    ./client.py

