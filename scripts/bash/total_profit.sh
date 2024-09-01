cat games.csv| csvcut -c 5 | awk '{sum += $1} END {print sum}'
