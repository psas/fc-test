FCBIN="../av3-fc"
TELEM="../../Ground/telemetry/"

setup:
	ln -s $(FCBIN) ./av3-fc
	ln -s $(TELEM) ./telemetry

clean:
	unlink ./av3-fc
	unlink ./telemetry
