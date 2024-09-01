import re
from decimal import Decimal

NUMBER_PATTERN = r'[0-9]+(?:\.\d{2})?'
MY_NAME = r'\[ME\]'
STACK_EXPRESSION =r'^.*:\s+(?P<position>.*)\s+\[ME\]\s+\(\$(?P<stack_size>' + NUMBER_PATTERN + r') in chips\)'

def get_amount(action):
    # pattern = r'^.*\$(' + NUMBER_PATTERN + r').*$'
    pattern = r'\$(' + NUMBER_PATTERN + r')'
    amount = re.search(pattern, action).group()
    return Decimal(amount.replace('$', ''))


def process_line(line, curr_hand):
    line = line.strip()
    if re.search(r'\[ME\]', line):
        result = re.match(STACK_EXPRESSION, line)
        if result is not None:  

                result_dict = result.groupdict()
                curr_hand = {
                    "stack_size": result_dict['stack_size'],
                    "position": result_dict['position'],
                    "hand": None,
                    "showdown": None,
                    "hand_rank": None,
                    "net": Decimal(0)
                }
                return curr_hand
        else:
            action = re.sub(r'.*:\s+(.*)', r'\1', line)

            if re.search(r'Card dealt', action, re.IGNORECASE):
                curr_hand["hand"] = re.sub(r'.*:.*\[(.*)\]', r'\1', line)

            elif re.search(r'Showdown', action):
                pattern = r'Showdown \[(?P<showdown>.*)\] \((?P<hand_rank>.*)\)'
                result = re.match(pattern, action).groupdict()
                curr_hand["showdown"] = result["showdown"]
                curr_hand["hand_rank"] = result["hand_rank"]

            elif re.search(r'Posts|Blind|Bets|Raise|Calls|All-in', action, re.IGNORECASE):
                curr_hand["net"] -= Decimal(get_amount(action))
            
            elif re.search(r'Return|Hand result', action, re.IGNORECASE):
                curr_hand["net"] += Decimal(get_amount(action))
            
        
