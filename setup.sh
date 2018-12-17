#!/bin/bash
echo "#!/usr/bin/python3" > chord
cat python/chord.py >> chord
chmod 777 chord
sudo cp chord /usr/bin/chord
echo "Program setup completed"