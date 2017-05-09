"""
The query that must be executed and CSV dumped to be parsed through with this file

SELECT url,image_url,length(title),location_country,location_region,location_name,
location_type,length(sub_title),video_url,category,category_slug,currency,currency_symbol,
funding_goal,currently_raised,usd_currently_raised,state,end_date,launch_date,num_supporters,
num_updates,num_comments,campaign_state,length(story),num_fb_shares
FROM training_data
ORDER BY launch_date DESC
LIMIT 20;

"""

import csv
import timeit
url = ()
image_url = ()
title = ()
with open("test.csv", "r")as rfh, open("new_data.csv","a") as wfh:

        reader = csv.reader(rfh, delimiter=",")
        writer = csv.writer(wfh, delimiter=",")

        for cols in reader:
            if cols[0] != "":
                url = url + (1,)
            else:
                url = url + (0,)

            if cols[1] != "":
                image_url = image_url + (1,)
            else:
                image_url = image_url + (0,)

            if len(cols[2]) > 0:
                title = title + (1,)
            else:
                title = title + (0,)

print(len(url),len(image_url),len(title))
print(url,image_url,title)
print("Execution time was {0}".format(timeit.timeit()))