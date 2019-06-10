import pandas as pd
import json
from scrapy.http import TextResponse
import numpy as np
import requests
import urllib

def review_details(customer_info,data_review,final_list):
    try:
        final_list.append(data_review['ContextDataValues'][customer_info]['Value'])
    except:
        final_list.append(None)

    return final_list

def get_reviews(product_df):

    product_id_review =[]
    user_id = []
    user_rating = []
    user_skintype = []
    user_eyecolor = []
    user_haircolor = []
    user_skintone = []
    user_age = []
    avg_score = []

    num_of_reviews_for_json = product_df['total_reviews'].tolist()
    product_id_for_json = product_df['p_id'].tolist()

    for i in range(len(product_id_for_json)):
        print(i)
        link3 = 'https://api.bazaarvoice.com/data/reviews.json?Filter=ProductId%3A' +\
                  product_id_for_json[i] + '&Sort=Helpfulness%3Adesc&Limit=' +'{}&Offset={}&Include=Products%2CComments&'.format(min(int(num_of_reviews_for_json[i]), int(100)), 0) +\
              'Stats=Reviews&passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4'
        print(link3)
        with urllib.request.urlopen(link3) as url:
            data = json.loads(url.read().decode())
            try:
                first_key = list(data['Includes']['Products'].keys())[0]
            except:
                continue

            for j in range(len(data['Results'])):
                product_id_review.append(product_id_for_json[i])

                try:
                    dict_sum = data['Includes']['Products'][first_key]['ReviewStatistics']
                    avg_score.append(dict_sum['AverageOverallRating'])
                except:
                    avg_score.append(None)

                try:
                    user_id.append(data['Results'][j]['UserNickname'])
                except:
                    user_id.append(None)
                try:
                    user_rating.append(data['Results'][j]['Rating'])
                except:
                    user_rating.append(None)
                user_skintype = review_details('skinType',data['Results'][j],user_skintype)
                user_eyecolor = review_details('eyeColor',data['Results'][j],user_eyecolor)
                user_haircolor = review_details('hairColor',data['Results'][j],user_haircolor)
                user_skintone = review_details('skinTone',data['Results'][j],user_skintone)
                user_age = review_details('age',data['Results'][j],user_age)

    ind_review_df_temp = pd.DataFrame({'user_id': user_id,'product_id':product_id_review,'avg_score':avg_score,'user_rating': user_rating,\
                      'user_skintype': user_skintype,'user_eyecolor': user_eyecolor,'user_haircolor': user_haircolor,\
                     'user_skintone': user_skintone,'user_age':user_age})

    ind_review_df = ind_review_df_temp[ind_review_df_temp.user_id.notnull()]
    ind_review_df.reset_index(drop=True)

    eyecolor_set = ind_review_df.user_eyecolor.unique().tolist()
    haircolor_set = ind_review_df.user_haircolor.unique().tolist()
    skintone_set = ind_review_df.user_skintone.unique().tolist()

    eyecolor_set[[i for i, val in enumerate(eyecolor_set) if val == None][0]] = 'None'
    haircolor_set[[i for i, val in enumerate(haircolor_set) if val == None][0]] = 'None'
    skintone_set[[i for i, val in enumerate(skintone_set) if val == None][0]] = 'None'

    demo_list= []
    for line in ind_review_df.itertuples():
        demo_list.append(str(eyecolor_set.index(str(line[6]))) + str(haircolor_set.index(str(line[7]))) + str(skintone_set.index(str(line[8]))))
    ind_review_df['demo'] = demo_list

    return ind_review_df
