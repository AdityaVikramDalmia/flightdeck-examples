.PHONY: test smoke demo

test:
	@bash tests/smoke.sh

smoke: test

demo:
	@bash examples/end-to-end-demo.sh
