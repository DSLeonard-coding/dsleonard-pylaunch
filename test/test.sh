rm -rf test-projects
mkdir test-projects
if [ ! -e replay.json ]; then
cookiecutter  -f  ../ -o test-projects ; cp ~/.cookiecutter_replay/pylaunch.json replay.json -f
else
cookiecutter --replay --replay-file replay.json -f ../ -o test-projects
fi
