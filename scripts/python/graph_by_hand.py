import pandas as pd
import matplotlib.pyplot as plt
import sys


def convert_card_value(card_value):
    # Split the card value into rank and suit
    rank1, suit1 = card_value[0], card_value[1]
    rank2, suit2 = card_value[3], card_value[4]
    
    # Convert the ranks to their symbols
    converted_value = rank1 + rank2
    
    
    char_list = list(converted_value)
    char_list_sorted = sorted(char_list)
    sorted_string = ''.join(char_list_sorted)

    # Determine if the cards are suited or not
    if suit1 == suit2:
        sorted_string += '+'
    
    return sorted_string

# Load the CSV file
file_path = sys.argv[1]
data = pd.read_csv(file_path)

data['hand_val'] = data['hand'].apply(convert_card_value)


grouped = data.groupby('hand_val')
sum_df = grouped['net'].sum()
count_df = grouped.size()

# Combine the results into a single DataFrame
result_df = pd.DataFrame({
    'net_sum': sum_df,
    'count': count_df
}).reset_index()

result_df['avg. profitability'] = result_df['net_sum'] / result_df['count']

result_df['net_sum'] = result_df['net_sum'].round(2)
result_df['avg. profitability'] = result_df['avg. profitability'].round(2)

result_df = result_df.sort_values('avg. profitability')

result_df.to_csv('hand_profitability.csv', index=False)