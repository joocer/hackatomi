lint:
	python -m pip install --quiet --upgrade pycln isort black yamllint
#	python -m yamllint .
	python -m pycln .
	python -m isort .
	python -m black .

update:
	python -m pip install --upgrade pip
	python -m pip install --upgrade -r requirements.txt

run-bonnie:
	clear
	python /Users/justin/Nextcloud/mabel/hakatomi/bonnie/bonnie.py

run-gruber:
	clear
	python /Users/justin/Nextcloud/mabel/hakatomi/gruber/gruber.py

run-web:
	clear
	cd /Users/justin/Nextcloud/mabel/hakatomi/web
	python -m http.server 8085