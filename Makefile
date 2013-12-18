FCBIN="../av3-fc"
TELEM="../../Ground/telemetry/"

all: clean build

setup:
	ln -s $(FCBIN) ./av3-fc
	ln -s $(TELEM) ./telemetry

build:
	coffee -c -o test-app/static/js test-app/static/src/*.coffee

cleanlinks:
	unlink ./av3-fc
	unlink ./telemetry

clean:
	rm -f static/js/*.js

rmlogs:
	rm -f logfile-*
