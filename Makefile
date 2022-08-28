init:
	pip install -r requirements.txt

test_algorithm:
	python3 algorithm.py

test_code:
	python3 test_driver.py

setup_environment:
	conda activate automated-hvf-grading
