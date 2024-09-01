
flit:
	# flit install --symlink --python rel-venv/bin/python3
	flit install --python rel-venv/bin/python3

pyinstaller-init:
	pyinstaller ./pyzzz/server/main.py
	# pyinstaller --paths rel-venv/lib/python3.12/site-packages ./pyzzz/server/main.py
	#
pyinstaller:
	pyinstaller ./main.spec
