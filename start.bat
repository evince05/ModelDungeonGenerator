docker build -t cisc204 .
docker run -it -v "%cd%":/PROJECT cisc204 /bin/bash -c "python3 run.py"
python3 --version
PAUSE

