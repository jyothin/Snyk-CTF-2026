#!/bin/zsh
echo $1
john --wordlist=~/GitHub-jyothin/SecLists/$1 hash-my.txt
john --show hash-my.txt

