
runpy:
	rel-venv/bin/python3 -m pyzzz.server.main --reload pyzzz

flit:
	flit install --python rel-venv/bin/python3

compile:
	rel-venv/bin/python3 -m nuitka --follow-imports ./pyzzz/server/main.py
	mv main.bin main.exe
