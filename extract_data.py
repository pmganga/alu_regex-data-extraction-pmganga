#!/usr/bin/env python3
# Philip - regex assignment for ALU
# I tried to make this extract emails, urls, phones, credit cards and times
# Also check if input looks dangerous

import re
import sys

# this function checks if credit card is real using Luhn
def check_luhn(card_number):
    # remove spaces and dashes first
    digits = re.sub(r'[^0-9]', '', card_number)
    
    if len(digits) != 16:
        return False
        
    total = 0
    # go from right to left
    for i in range(len(digits)-1, -1, -1):
        num = int(digits[i])
        if (len(digits) - i) % 2 == 0:  # every second from right
            num = num * 2
            if num > 9:
                num = num - 9
        total = total + num
    
    if total % 10 == 0:
        return True
    else:
        return False

# hide most of the credit card number
def hide_card_number(card):
    clean = re.sub(r'[^0-9]', '', card)
    if len(clean) != 16:
        return clean  # just return if wrong length
    return "**** **** **** " + clean[-4:]

def find_all_data(text):
    # first check if this looks like bad input
    bad_patterns = [
        "<script",
        "</script>",
        "drop table",
        "union select",
        "--",
        "; --"
    ]
    
    for bad in bad_patterns:
        if re.search(bad, text, re.IGNORECASE):
            return "Unsafe input! Possible attack. Stopping now."
    
    # now try to find different things
    results = {}
    
    # emails - I copied this pattern from internet and changed a bit
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    if emails:
        results["Emails"] = [e.strip() for e in emails]
    
    # urls - this one was hard, I hope it works
    url_pattern = r'(https?://)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/\S*)?'
    urls = re.findall(url_pattern, text)
    if urls:
        clean_urls = []
        for u in urls:
            # because findall gives tuple sometimes
            if isinstance(u, tuple):
                clean_urls.append("".join(u).strip())
            else:
                clean_urls.append(u.strip())
        results["URLs"] = clean_urls
    
    # phone numbers - this is messy but I think it catches most
    phone_pattern = r'(\+?\d{1,3}[- ]?)?(\(\d{3}\)|\d{3})[- ]?\d{3}[- ]?\d{4}'
    phones = re.findall(phone_pattern, text)
    if phones:
        phone_list = []
        for p in phones:
            full = "".join(p)
            digits = re.sub(r'\D', '', full)
            if len(digits) == 10:
                digits = "+1" + digits
            phone_list.append(digits)
        results["Phone Numbers"] = phone_list
    
    # credit cards - 16 digits with spaces or dashes
    card_pattern = r'\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}'
    cards = re.findall(card_pattern, text)
    if cards:
        valid_cards = []
        for c in cards:
            if check_luhn(c):
                hidden = hide_card_number(c)
                valid_cards.append(hidden)
        if valid_cards:
            results["Credit Cards"] = valid_cards
    
    # times - 24h and 12h with AM/PM
    time_pattern = r'([01]?\d|2[0-3]):[0-5]\d(\s*[AP]M)?'
    times = re.findall(time_pattern, text)
    if times:
        time_list = []
        for t in times:
            time_list.append("".join(t).strip())
        results["Times"] = time_list
    
    if not results:
        return "Nothing useful found."
    
    return results

# main part
if __name__ == "__main__":
    text_to_check = ""
    
    # check if file name given
    if len(sys.argv) > 1:
        try:
            f = open(sys.argv[1], 'r')
            text_to_check = f.read()
            f.close()
        except:
            print("Cannot open file!")
            sys.exit()
    else:
        # read from keyboard
        text_to_check = sys.stdin.read()
    
    # print("DEBUG: input length =", len(text_to_check))  # I left this for testing
    
    output = find_all_data(text_to_check)
    
    if isinstance(output, str):
        print(output)
    else:
        for category in output:
            print(category + ":")
            for item in output[category]:
                print("  - " + item)
