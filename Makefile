FCBIN="../av3-fc"
TELEM="../../Ground/telemetry/"

all: clean build

setup:
	ln -s $(FCBIN) ./av3-fc
	ln -s $(TELEM) ./telemetry

build:
	coffee -c -o mobile-device-test/static/js mobile-device-test/static/src/*.coffee

cleanlinks:
	unlink ./av3-fc
	unlink ./telemetry

clean:
	rm -f static/js/*.js
