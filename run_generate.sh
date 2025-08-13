python3 generate_all_tasks.py --count 2000 --split train --output training_data --tasks maze

python3 generate_all_tasks.py --count 1000 --split test --output evaluation_data

python check_data_leakage.py --eval-root evaluation_data --train-root training_data --output-root evaluation_data_clean