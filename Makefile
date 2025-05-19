init:
	uv sync

run:
	EKARTOTEKA_AUTHORIZATION=$(shell cat .env | grep EKARTOTEKA_AUTHORIZATION | cut -d '=' -f2)
	EKARTOTEKA_COOKIE=$(shell cat .env | grep EKARTOTEKA_COOKIE | cut -d '=' -f2)
	uv run src/main.py
