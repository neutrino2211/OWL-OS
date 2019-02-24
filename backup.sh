#! /bin/bash

# echo "What do you want to save it as ? "

read -p "What do you want to save it as ? " location

user=$(whoami)

# echo "External drive ? "

read -p "External drive ? " drive

zip -r "$location" .

mv $location.zip /media/$user/$drive
