import csv
from textblob import TextBlob

# define a function to perform sentiment analysis on a string
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# open the input CSV file for reading and the output CSV file for writing
with open('headlines.csv', 'r') as csvfile, open('output.csv', 'w', newline='') as outfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(outfile)

    # write the header row for the output CSV file
    header_row = next(reader)
    header_row.append('sentiment')
    writer.writerow(header_row)

    # loop through each row in the input CSV file
    for row in reader:
        # perform sentiment analysis on the headline
        headline = row[1]
        sentiment = get_sentiment(headline)

        # write the row with the sentiment grade added as a new column
        row.append(sentiment)
        writer.writerow(row)
