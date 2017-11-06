import csv
import requests

for service in ['twitter', 'soundcloud', 'instagram', 'facebook']:
    CSV_URL = f'https://s3-us-west-1.amazonaws.com/burn-cartel-content/{service}.csv'
    with requests.Session() as s:
        # write to local csv stuffz
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            print(row)
