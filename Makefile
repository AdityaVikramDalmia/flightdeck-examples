.PHONY: test smoke demo

test:
	@python3 tests/clone_all.py
	@bash tests/smoke.sh

smoke: test

demo:
	@bash examples/end-to-end-demo.sh
