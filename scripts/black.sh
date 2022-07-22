PYFILES=$(find . -path ./venv -prune -o -name '*.py' -print)

for PYFILE in $PYFILES; do
    black $PYFILE
done
