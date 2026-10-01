all: run
run:
	python experiments/run_all.py --seed 42 --live
test:
	pytest -q tests/
docker:
	docker compose up --build lab
verify:
	docker compose --profile verify up --build verify
