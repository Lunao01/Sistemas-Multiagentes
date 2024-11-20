#/bin/sh

# maybe datasetscan is not needed, since it will only run once, it shouldnt be too wasteful to program it as a separate container
python datasetscan.py &
fastapi run /app/imgfetcher.py