# FC Test Framework


This contains a Procfile other setup info that can bring up the entire flight
computer in a test environment in one command.


## Install Steps:

### Get dependencies

Make sure you have the flight computer code and the telemetry viewer

 - FC: <https://github.com/psas/av3-fc>
 - Telemetry: <https://github.com/psas/telemetry>

Make sure you can build and run the FC and telemetry framework on their own.


### Build links

Edit the Makefile to change `FCBIN` and `TELEM` variables to point towards the location where you cloned the above on your machine.

	$ make setup


### Build test app

Generate javascript for the test control panel. Make sure you have coffeescript

    $ sudo apt-get install nodejs npm
    $ sudo npm install coffee
    $ make build


### Python environment

Make a virtual env and install the requirements

    $ mkvirtualenv fctest
    (fctest)$ pip install -r requirements.txt
 

## Run

Once you have everything set up continue to develop back as normal. When you
need to run the FC as a full test simply come here and run

	(fctest)$ ./run

## Usage

Open browser pages to:

 - <localhost:5000> (the control panel)
 - <localhost:8080> (telemetry)

## Finish and Resume

When you're finished, kill the script with Ctrl+C and get out of the virtualenv with `deactivate`.

To resume the environment, navigate back to this directory and run `workon fctest`.
