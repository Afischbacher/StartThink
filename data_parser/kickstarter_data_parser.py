"""
data_parser query

use crowdfund;
SELECT url,
image_url,
length(title),
location_country,
location_type,
length(sub_title),
video_url,
category,
category_slug,
currency,
funding_goal,
state,
end_date,
launch_date,
num_supporters,
num_updates,
num_comments,
length(story),
num_fb_shares,
REPLACE(REPLACE(REPLACE(story,'\n',''), '\t',''),';',''),
REPLACE(REPLACE(REPLACE(title,'\n',''), '\t',''),';',''),
REPLACE(REPLACE(REPLACE(sub_title,'\n',''), '\t',''),';',''),
REPLACE(rewards,";", ""),
usd_currently_raised
FROM training_data
WHERE state = "successful" OR state = "failed"
ORDER BY launch_date DESC
LIMIT 23200;


- length of title : 79 (That is our baseline for 1)
- length of sub_title : 249 (That is our baseline for 1)
- length of story : 57275 (That is our baseline for 1)
- size of funding goal: 172,266 (That is our baseline for 1 which is the average funding goal,
times 2 standard deviations to the left)
- size of num_supporters: 998 (That is our baseline for 1)
- size of num_updates: 93 (That is our baseline for 1)
- size of num_comments: 998 (That is our baseline for 1)
- size of nun_fb_shares: 235648 (That is our baseline for 1)
- size of currently_raised_max value = SQL statement dump

MAX LAUNCH DATE UNIX TIME = 1493817026
MAX END DATE UNIX TIME = 1496534975

Baseline for 1 with Duration of Campaign = 2717949 // 31.45774 Days

Input Layer (Last 4 nodes)

-	US_Currently_Raised
-	State of Success / Failure
-	FB Shares
-	# of Supporters

"""
import time
import datetime
import csv
import json
from textblob import TextBlob

time_start = time.time()


def data_parser():
    location_country_dict = {
        'AE': 0,
        'AF': 0,
        'AG': 0,
        'AM': 0,
        'AQ': 0,
        'AR': 0,
        'AT': 0,
        'AU': 0,
        'BA': 0,
        'BB': 0,
        'BE': 0,
        'BF': 0,
        'BG': 0,
        'BO': 0,
        'BQ': 0,
        'BR': 0,
        'BS': 0,
        'BW': 0,
        'BY': 0,
        'BZ': 0,
        'CA': 0,
        'CH': 0,
        'CL': 0,
        'CM': 0,
        'CN': 0,
        'CO': 0,
        'CR': 0,
        'CU': 0,
        'CW': 0,
        'CY': 0,
        'CZ': 0,
        'DE': 0,
        'DJ': 0,
        'DK': 0,
        'DM': 0,
        'DO': 0,
        'EC': 0,
        'EE': 0,
        'EG': 0,
        'ES': 0,
        'ET': 0,
        'FI': 0,
        'FM': 0,
        'FR': 0,
        'GB': 0,
        'GE': 0,
        'GH': 0,
        'GL': 0,
        'GP': 0,
        'GR': 0,
        'GT': 0,
        'GU': 0,
        'GY': 0,
        'HK': 0,
        'HN': 0,
        'HR': 0,
        'HT': 0,
        'HU': 0,
        'ID': 0,
        'IE': 0,
        'IL': 0,
        'IN': 0,
        'IQ': 0,
        'IR': 0,
        'IS': 0,
        'IT': 0,
        'JM': 0,
        'JP': 0,
        'KE': 0,
        'KG': 0,
        'KH': 0,
        'KR': 0,
        'KW': 0,
        'KZ': 0,
        'LA': 0,
        'LB': 0,
        'LI': 0,
        'LK': 0,
        'LT': 0,
        'LU': 0,
        'LV': 0,
        'MA': 0,
        'MC': 0,
        'MD': 0,
        'ME': 0,
        'MG': 0,
        'MK': 0,
        'MM': 0,
        'MN': 0,
        'MT': 0,
        'MX': 0,
        'MY': 0,
        'MZ': 0,
        'NA': 0,
        'NG': 0,
        'NI': 0,
        'NL': 0,
        'NO': 0,
        'NP': 0,
        'NZ': 0,
        'PA': 0,
        'PE': 0,
        'PG': 0,
        'PH': 0,
        'PK': 0,
        'PL': 0,
        'PR': 0,
        'PT': 0,
        'PY': 0,
        'RO': 0,
        'RS': 0,
        'RU': 0,
        'RW': 0,
        'SE': 0,
        'SG': 0,
        'SI': 0,
        'SJ': 0,
        'SK': 0,
        'SL': 0,
        'SN': 0,
        'SO': 0,
        'SR': 0,
        'SV': 0,
        'TH': 0,
        'TN': 0,
        'TO': 0,
        'TR': 0,
        'TT': 0,
        'TW': 0,
        'TZ': 0,
        'UA': 0,
        'UG': 0,
        'US': 0,
        'UY': 0,
        'VC': 0,
        'VE': 0,
        'VI': 0,
        'VN': 0,
        'YE': 0,
        'ZA': 0,
        'ZM': 0,
        'ZW': 0

    }

    category_dict = {
        'Horror': 0,
        'Comedy': 0,
        'Apps': 0,
        'Product Design': 0,
        'Mixed Media': 0,
        'Comic Books': 0,
        'Tabletop Games': 0,
        'Zines': 0,
        'Music Videos': 0,
        'Rock': 0,
        'Radio & Podcasts': 0,
        'Immersive': 0,
        'Playing Cards': 0,
        'Shorts': 0,
        'Crafts': 0,
        'Fine Art': 0,
        'Drinks': 0,
        'Festivals': 0,
        'Documentary': 0,
        'Video Games': 0,
        'Children&#39;s Books': 0,
        'Country & Folk': 0,
        'Gadgets': 0,
        'Music': 0,
        'Experimental': 0,
        'Technology': 0,
        'Footwear': 0,
        'Art': 0,
        'Print': 0,
        'Theater': 0,
        'Ready-to-wear': 0,
        'Photography': 0,
        'Webseries': 0,
        'Restaurants': 0,
        'Web': 0,
        'Design': 0,
        'Games': 0,
        'Fashion': 0,
        'Nonfiction': 0,
        'Fiction': 0,
        'Live Games': 0,
        'Indie Rock': 0,
        '3D Printing': 0,
        'Software': 0,
        'Apparel': 0,
        'Farms': 0,
        'Public Art': 0,
        'Woodworking': 0,
        'Hardware': 0,
        'Photobooks': 0,
        'Illustration': 0,
        'Publishing': 0,
        'Calendars': 0,
        'Film & Video': 0,
        'Gaming Hardware': 0,
        'Flight': 0,
        'Graphic Novels': 0,
        'Architecture': 0,
        'Spaces': 0,
        'Metal': 0,
        'Food': 0,
        'Cookbooks': 0,
        'Hip-Hop': 0,
        'Art Books': 0,
        'Thrillers': 0,
        'People': 0,
        'Pop': 0,
        'Anthologies': 0,
        'Camera Equipment': 0,
        'Science Fiction': 0,
        'Narrative Film': 0,
        'Television': 0,
        'Accessories': 0,
        'World Music': 0,
        'Photo': 0,
        'Animation': 0,
        'Painting': 0,
        'Comics': 0,
        'Webcomics': 0,
        'Space Exploration': 0,
        'Installations': 0,
        'Graphic Design': 0,
        'Mobile Games': 0,
        'Faith': 0,
        'Drama': 0,
        'DIY': 0,
        'Young Adult': 0,
        'Stationery': 0,
        'Sound': 0,
        'Performances': 0,
        'Small Batch': 0,
        'Electronic Music': 0,
        'Civic Design': 0,
        'Punk': 0,
        'Jazz': 0,
        'Conceptual Art': 0,
        'Audio': 0,
        'Academic': 0,
        'Ceramics': 0,
        'Musical': 0,
        'Dance': 0,
        'Classical Music': 0,
        'Fabrication Tools': 0,
        'Interactive Design': 0,
        'Places': 0,
        'Plays': 0,
        'R&B': 0,
        'Family': 0,
        'Jewelry': 0,
        'Sculpture': 0,
        'Wearables': 0,
        'Candles': 0,
        'DIY Electronics': 0,
        'Performance Art': 0,
        'Video': 0,
        'Printing': 0,
        'Quilts': 0,
        'Food Trucks': 0,
        'Journalism': 0,
        'Events': 0,
        'Literary Journals': 0,
        'Typography': 0,
        'Childrenswear': 0,
        'Blues': 0,
        'Translations': 0,
        'Fantasy': 0,
        'Periodicals': 0,
        'Poetry': 0,
        'Couture': 0,
        'Makerspaces': 0,
        'Vegan': 0,
        'Pet Fashion': 0,
        'Workshops': 0,
        'Action': 0,
        'Textiles': 0,
        'Crochet': 0,
        'Romance': 0,
        'Robots': 0,
        'Community Gardens': 0,
        'Digital Art': 0,
        'Puzzles': 0,
        'Nature': 0,
        'Pottery': 0,
        'Animals': 0,
        'Kids': 0,
        'Movie Theaters': 0,
        'Embroidery': 0,
        'Latin': 0,
        'Farmer&#39;s Markets': 0,
        'Glass': 0,
        'Bacon': 0,
        'Video Art': 0,
        'Weaving': 0,
        'Knitting': 0,
        'Residencies': 0,
        'Taxidermy': 0,
        'Letterpress': 0,
        'Literary Spaces': 0,
        'Chiptune': 0,

    }

    location_type_dict = {
        'Town': 0,
        'County': 0,
        'Suburb': 0,
        'Zip': 0,
        'LocalAdmin': 0,
        'Island': 0,
        'Country': 0,
        'Miscellaneous': 0,
        'Estate': 0

    }

    category_slug_dict = {

        'art': 0,
        'art/ceramics': 0,
        'art/conceptual art': 0,
        'art/digital art': 0,
        'art/illustration': 0,
        'art/installations': 0,
        'art/mixed media': 0,
        'art/painting': 0,
        'art/performance art': 0,
        'art/public art': 0,
        'art/sculpture': 0,
        'art/textiles': 0,
        'art/video art': 0,
        'comics': 0,
        'comics/anthologies': 0,
        'comics/comic books': 0,
        'comics/events': 0,
        'comics/graphic novels': 0,
        'comics/webcomics': 0,
        'crafts': 0,
        'crafts/candles': 0,
        'crafts/crochet': 0,
        'crafts/diy': 0,
        'crafts/embroidery': 0,
        'crafts/glass': 0,
        'crafts/knitting': 0,
        'crafts/pottery': 0,
        'crafts/printing': 0,
        'crafts/quilts': 0,
        'crafts/stationery': 0,
        'crafts/taxidermy': 0,
        'crafts/weaving': 0,
        'crafts/woodworking': 0,
        'dance': 0,
        'dance/performances': 0,
        'dance/residencies': 0,
        'dance/spaces': 0,
        'dance/workshops': 0,
        'design': 0,
        'design/architecture': 0,
        'design/civic design': 0,
        'design/graphic design': 0,
        'design/interactive design': 0,
        'design/product design': 0,
        'design/typography': 0,
        'fashion': 0,
        'fashion/accessories': 0,
        'fashion/apparel': 0,
        'fashion/childrenswear': 0,
        'fashion/couture': 0,
        'fashion/footwear': 0,
        'fashion/jewelry': 0,
        'fashion/pet fashion': 0,
        'fashion/ready-to-wear': 0,
        'film & video': 0,
        'film & video/action': 0,
        'film & video/animation': 0,
        'film & video/comedy': 0,
        'film & video/documentary': 0,
        'film & video/drama': 0,
        'film & video/experimental': 0,
        'film & video/family': 0,
        'film & video/fantasy': 0,
        'film & video/festivals': 0,
        'film & video/horror': 0,
        'film & video/movie theaters': 0,
        'film & video/music videos': 0,
        'film & video/narrative film': 0,
        'film & video/romance': 0,
        'film & video/science fiction': 0,
        'film & video/shorts': 0,
        'film & video/television': 0,
        'film & video/thrillers': 0,
        'film & video/webseries': 0,
        'food': 0,
        'food/bacon': 0,
        'food/community gardens': 0,
        'food/cookbooks': 0,
        'food/drinks': 0,
        'food/events': 0,
        'food/farmer&#39;s markets': 0,
        'food/farms': 0,
        'food/food trucks': 0,
        'food/restaurants': 0,
        'food/small batch': 0,
        'food/spaces': 0,
        'food/vegan': 0,
        'games': 0,
        'games/gaming hardware': 0,
        'games/live games': 0,
        'games/mobile games': 0,
        'games/playing cards': 0,
        'games/puzzles': 0,
        'games/tabletop games': 0,
        'games/video games': 0,
        'journalism': 0,
        'journalism/audio': 0,
        'journalism/photo': 0,
        'journalism/print': 0,
        'journalism/video': 0,
        'journalism/web': 0,
        'music': 0,
        'music/blues': 0,
        'music/chiptune': 0,
        'music/classical music': 0,
        'music/comedy': 0,
        'music/country & folk': 0,
        'music/electronic music': 0,
        'music/faith': 0,
        'music/hip-hop': 0,
        'music/indie rock': 0,
        'music/jazz': 0,
        'music/kids': 0,
        'music/latin': 0,
        'music/metal': 0,
        'music/pop': 0,
        'music/punk': 0,
        'music/r&b': 0,
        'music/rock': 0,
        'music/world music': 0,
        'photography': 0,
        'photography/animals': 0,
        'photography/fine art': 0,
        'photography/nature': 0,
        'photography/people': 0,
        'photography/photobooks': 0,
        'photography/places': 0,
        'publishing': 0,
        'publishing/academic': 0,
        'publishing/anthologies': 0,
        'publishing/art books': 0,
        'publishing/calendars': 0,
        'publishing/children&#39;s books': 0,
        'publishing/comedy': 0,
        'publishing/fiction': 0,
        'publishing/letterpress': 0,
        'publishing/literary journals': 0,
        'publishing/literary spaces': 0,
        'publishing/nonfiction': 0,
        'publishing/periodicals': 0,
        'publishing/poetry': 0,
        'publishing/radio & podcasts': 0,
        'publishing/translations': 0,
        'publishing/young adult': 0,
        'publishing/zines': 0,
        'technology': 0,
        'technology/3d printing': 0,
        'technology/apps': 0,
        'technology/camera equipment': 0,
        'technology/diy electronics': 0,
        'technology/fabrication tools': 0,
        'technology/flight': 0,
        'technology/gadgets': 0,
        'technology/hardware': 0,
        'technology/makerspaces': 0,
        'technology/robots': 0,
        'technology/software': 0,
        'technology/sound': 0,
        'technology/space exploration': 0,
        'technology/wearables': 0,
        'technology/web': 0,
        'theater': 0,
        'theater/comedy': 0,
        'theater/experimental': 0,
        'theater/festivals': 0,
        'theater/immersive': 0,
        'theater/musical': 0,
        'theater/plays': 0,
        'theater/spaces': 0
    }

    currency_dict = {
        'AUD': 0,
        'CAD': 0,
        'CHF': 0,
        'DKK': 0,
        'EUR': 0,
        'GBP': 0,
        'HKD': 0,
        'MXN': 0,
        'NOK': 0,
        'NZD': 0,
        'SEK': 0,
        'SGD': 0,
        'USD': 0
    }

    baseline_title = 79
    baseline_sub_title = 249
    baseline_of_story = 57275
    baseline_of_funding_goal = 172266
    baseline_of_num_supporters = 998
    baseline_of_num_updates = 93
    baseline_of_num_comments = 998
    baseline_of_fb_shares = 235648
    baseline_of_campaign_duration = 2717949
    baseline_of_currently_raised = 12393140
    baseline_of_max_rewards = 200000
    baseline_of_max_num_rewards = 55

    with open("data_test.csv", "r")as rfh, open("machine_learning_data_kickstarter.csv", "w+") as wfh:
        reader = csv.reader(rfh, delimiter=";", quotechar='"')
        writer = csv.writer(wfh, delimiter=";", quoting=csv.QUOTE_NONE, escapechar=" ")
        next(reader, None)
        for cols in reader:

            url = ()
            image_url = ()
            title = ()
            location_country = ()
            location_type = ()
            sub_title = ()
            video_url = ()
            category = ()
            category_slug = ()
            currency = ()
            funding_goal = ()
            currently_raised = ()
            campaign_state = ()
            num_supporters = ()
            duration_of_campaign = ()
            num_updates = ()
            num_comments = ()
            length_story = ()
            num_fb_shares = ()
            story_sentiment = 0
            title_sentiment = 0
            sub_title_sentiment = 0
            num_of_rewards = ()
            len_of_rewards = ()
            avg_rewards = 0
            usd_funding_raised = 0

            if cols[0] != "" and cols[0] != "NULL":
                url = 1
            else:
                url = 0

            if cols[1] != "" and cols[1] != "NULL":
                image_url = 1
            else:
                image_url = 0

            if len(cols[2]) > 0 and cols[2] != "NULL":
                title = (int(cols[2]) / int(baseline_title))
            else:
                title = 0

            for k in location_country_dict:
                if k == cols[3]:
                    location_country_dict[cols[3]] = 1
                    for k, v in location_country_dict.items():
                        location_country = location_country + (v,)

            for k in location_type_dict:
                if k == cols[4]:
                    location_type_dict[cols[4]] = 1
                    for k, v in location_type_dict.items():
                        location_type = location_type + (v,)

            if len(cols[5]) > 0 and cols[5] != "NULL":
                sub_title = (int(cols[5]) / int(baseline_sub_title))
            else:
                sub_title = 0

            if cols[6] != "" and cols[6] != "NULL":
                video_url = 1
            elif cols[6] == "NULL":
                video_url = 0

            for k in category_dict:
                if k == cols[7]:
                    category_dict[cols[7]] = 1
                    for k, v in category_dict.items():
                        category = category + (v,)

            for k in category_slug_dict:
                if k == cols[8]:
                    category_slug_dict[cols[8]] = 1
                    for k, v in category_slug_dict.items():
                        category_slug = category_slug + (v,)

            for k in currency_dict:
                if k == cols[9]:
                    currency_dict[cols[9]] = 1
                    for k, v in currency_dict.items():
                        currency = currency + (v,)

            if len(cols[10]) > 0 and cols[10] != "NULL":
                funding_goal = (int(cols[10]) / int(baseline_of_funding_goal))

            if cols[11] == str("successful").lower() and cols[11] != "NULL":
                campaign_state = (1)

            else:
                campaign_state = (0)

            if cols[12] != "" and cols[13] != "" and cols[12] != "NULL" and cols[13] != "NULL":
                start_time = time.mktime(
                    datetime.datetime.strptime(str(cols[13]), '%Y-%m-%d  %H:%M:%S').timetuple())
                end_time = time.mktime(datetime.datetime.strptime(str(cols[12]), '%Y-%m-%d  %H:%M:%S').timetuple())

                duration_of_campaign = (int(end_time - start_time) / int(baseline_of_campaign_duration))

            if int(cols[14]) > 0 and cols[14] != "NULL":
                num_supporters = (int(cols[14]))
            else:
                num_supporters = 0

            if int(cols[15]) >= 0 and cols[15] != "NULL":
                num_updates = (int(cols[15]) / baseline_of_num_updates)
            else:
                num_updates = 0

            if int(cols[16]) > 0 and cols[16] != "NULL":
                num_comments = (int(cols[16]) / baseline_of_num_comments)
            else:
                num_comments = 0

            if len(cols[17]) > 0 and cols[17] != "NULL":
                length_story = (len(cols[17]) / baseline_of_story)
            else:
                length_story = 0

            if int(cols[18]) >= 0 and cols[18] != "NULL":
                num_fb_shares = int(cols[18])
            else:
                num_fb_shares = 0

            if len(cols[19]) > 0:
                story_sentiment = TextBlob(str(cols[19]))

            else:
                story_sentiment = 0

            if len(cols[20]) > 0:
                title_sentiment = TextBlob(str(cols[20]))

            else:
                title_sentiment = 0

            if len(cols[21]) > 0:
                sub_title_sentiment = TextBlob(str(cols[21]))

            else:
                sub_title_sentiment = 0

            if len(cols[22]) > 0:
                data = str(cols[22])
                data = data[:2] + '"' + data[2:]
                if data.endswith('"'):
                    data = data[:-1]

                try:
                    json_data = json.loads(str(data))
                except json.decoder.JSONDecodeError as e:
                    continue

                rewards = []
                for iter in json_data:
                    rewards.append(iter['minimum'])
                    len_of_rewards = len_of_rewards + (len(json_data),)

                num_of_rewards = int(len_of_rewards / baseline_of_max_num_rewards)
                avg_rewards = int((sum(rewards) / len(rewards)) / baseline_of_max_rewards)


            else:
                num_of_rewards = 0

            if cols[23] != 0 or cols[23] !="NULL":
                usd_funding_raised = int(cols[23])

            writer.writerow(
                [
                    str(url) + "," + str(image_url) + "," + str(title) + ','.join(
                        map(str, location_country)) + ','.join(
                        map(str, location_type)) + ',' + str(sub_title) + ',' + str(
                        video_url) + ','.join(map(str, category)) + ','.join(map(str, category_slug)) + ','.join(
                        map(str, currency)) + "," + str(funding_goal) + ',' + str(duration_of_campaign) + "," + str(
                        num_updates) + "," + str(num_comments) + "," + str(
                        length_story) + "," + str(story_sentiment.subjectivity) + "," + str(
                        title_sentiment.subjectivity) + "," + str(sub_title_sentiment.subjectivity) + "," + str(
                        ((story_sentiment.polarity + 1) / 2)) + "," +
                    str(((title_sentiment.polarity + 1) / 2)) + "," + str(
                        ((sub_title_sentiment.polarity + 1) / 2)) + "," + str(num_of_rewards) + ',' + str(
                        avg_rewards) + "," + str(campaign_state) + ',' + str(num_fb_shares) + "," + str(
                        num_supporters)]

            )

            url = ()
            image_url = ()
            title = ()
            location_country = ()
            location_type = ()
            sub_title = ()
            video_url = ()
            category = ()
            category_slug = ()
            currency = ()
            funding_goal = ()
            currently_raised = ()
            campaign_state = ()
            num_supporters = ()
            duration_of_campaign = ()
            num_updates = ()
            num_comments = ()
            length_story = ()
            num_fb_shares = ()
            story_sentiment = 0
            title_sentiment = 0
            sub_title_sentiment = 0
            num_of_rewards = ()
            avg_rewards = 0
            usd_funding_raised = 0

            for k in category_dict:
                category_dict[k] = 0

            for k in location_country:
                location_country_dict[k] = 0

            for k in location_type_dict:
                location_type_dict[k] = 0

            for k in category_slug_dict:
                category_slug_dict[k] = 0

            for k in currency_dict:
                currency_dict[k] = 0


data_parser()

time_end = time.time()
print("Done")
print("Processing Time {0}".format(time_end - time_start))
print()
