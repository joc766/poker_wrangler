import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys


def convert_card_value(card_value):
    # Split the card value into rank and suit
    rank1, suit1 = card_value[0], card_value[1]
    rank2, suit2 = card_value[3], card_value[4]
    
    # Convert the ranks to their symbols
    converted_value = rank1 + rank2
    
    # Determine if the cards are suited or not
    
    char_list = list(converted_value)
    char_list_sorted = sorted(char_list)
    sorted_string = ''.join(char_list_sorted)

    if suit1 == suit2:
        sorted_string += '+'

    return sorted_string

def heatmap(df: pd.DataFrame):
    # Sort the DataFrame by the hand values (optional based on your needs)
    # Define the reversed custom order
    order_dict = {
        '2': 1, '3': 2, '4': 3, '5': 4, '6': 5,
        '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10,
        'Q': 11, 'K': 12, 'A': 13
    }
    df.loc[["card1_order"]] = df['card1'].map(order_dict)
    df["card2_order"] = df['card2'].map(order_dict)
    df = df.sort_values(by=['card1_order', 'card2_order'], )
    # Pivot the DataFrame to create a matrix
    heatmap_data = df.pivot(index='card1_order', columns='card2_order', values='avg. profitability')
    return heatmap_data


# Load the CSV file
file_path = sys.argv[1]
data = pd.read_csv(file_path)

data['hand_val'] = data['hand'].apply(convert_card_value)
# Splitting the hand into two separate cards for better sorting

grouped = data.groupby('hand_val')
sum_df = grouped['net'].sum()
count_df = grouped.size()

# Combine the results into a single DataFrame
result_df = pd.DataFrame({
    'net_sum': sum_df,
    'count': count_df
}).reset_index()

result_df['card1'] = result_df['hand_val'].str[0]
result_df['card2'] = result_df['hand_val'].str[1]

result_df['avg. profitability'] = result_df['net_sum'] / result_df['count']

result_df['net_sum'] = result_df['net_sum'].round(2)
result_df['avg. profitability'] = result_df['avg. profitability'].round(2)

suited_df = result_df[result_df['hand_val'].str.contains(r'\+')]
unsuited_df = result_df[~result_df['hand_val'].str.contains(r'\+')]

heatmap_data = heatmap(suited_df)
# Create the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", cbar=True)

plt.title('Hand Value Heatmap')
plt.show()

