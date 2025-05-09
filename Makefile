nothing:

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

devinstall:
	make install
	python -m pip install -r requirements_dev.txt

run:
	PYTHONPATH=. python app/main.py

dockup:
	docker-compose up

unittest:
	echo "Implement me!"
