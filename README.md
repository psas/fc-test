# FC Test Framework


This contains a Procfile other setup info that can bring up the entire flight
computer in a test environment in one command.


## Install

Make sure you have the flight computer code and the telemetry viewer

 - FC: <https://github.com/psas/av3-fc>
 - Telemetry: <https://github.com/psas/telemetry>

Install [foreman](https://github.com/ddollar/foreman):

	$ sudo apt-get install foreman

Make sure you can build and run the FC and telemtry framework.

### Build links

Edit the Makefile to point towards the location where you cloned the other
two repos and run 

	$ make setup


## Run

Once you have everything set up continue to develop back as normal. When you
need to run the FC as a full test simply run

	$ foreman start

And it will bring up everything in order. `ctrl-c` will kill everything.
