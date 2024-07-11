#!/bin/bash

# Run the first Python script for 1 minute
python3 ~/oled/ft_matrix.py &  # The '&' runs it in the background
sleep 60  # Wait for 1 minute

# Terminate the first script
pkill -f "ft_matrix.py"

# Run the second Python script
python3 ~/oled/ft_sys.py

