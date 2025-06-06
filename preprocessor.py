import re
import pandas as pd

def preprocessor(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm))\s-\s(.+)'
    matches = re.findall(pattern, data)

    # Clean non-breaking spaces
    cleaned_matches = [(t.replace('\u202f', ' '), msg) for t, msg in matches]
    df = pd.DataFrame(cleaned_matches, columns=['date_time', 'Message'])

    users, messages = [], []
    user_pattern = r'^[\d\s()+-]+$'

    for message in df['Message']:
        parts = message.split(': ', 1)

        if len(parts) == 2:
            user_candidate, msg_text = parts[0].strip(), parts[1].strip()
            if re.match(user_pattern, user_candidate) or user_candidate:
                users.append(user_candidate)
                messages.append(msg_text)
            else:
                users.append('group_notification')
                messages.append(message.strip())
        else:
            users.append('group_notification')
            messages.append(message.strip())

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['Message'], inplace=True)

    # Convert date_time and extract components
    df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%y, %I:%M %p')
    df['date'] = df['date_time'].dt.date
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = df['date_time'].dt.time
    df['year'] = df['date_time'].dt.year
    df['month_num'] = df['date_time'].dt.month
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    df['day_name'] = df['date_time'].dt.day_name()

    # Create period bins
    df['period'] = df['hour'].apply(lambda h: f"{h:02d}-{'00' if h == 23 else f'{(h + 1)%24:02d}' }")

    return df