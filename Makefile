FCBIN="../av3-fc"

setup:
	ln -s $(FCBIN) ./av3-fc

clean:
	unlink ./av3-fc
