import requests
import product_links
import product_details
import review_details
import pandas as pd

column_names = ['links2','brand_names','product_names','p_id','ratings','price','total_shades','total_reviews','loves','shades_names','img']
product_df = pd.DataFrame([], columns=column_names)
for i in range(1,6):
    pagenum = str(i)
    print(pagenum)
    links2,brand_names,product_names,product_ids,ratings = product_links.product_info_layer1(str(i))
    p_price, num_color, p_num_reviews, p_loves, name_color,img = product_details.product_info_layer2(links2)

    product_df_temp = pd.DataFrame(list(zip(links2,brand_names,product_names,product_ids,ratings,\
                                    p_price, num_color, p_num_reviews, p_loves, name_color,img)), columns=column_names)

    product_df = product_df.append(product_df_temp, ignore_index=True)

'''filename = 'product_info_whole.csv'
product_df.to_csv(filename, encoding='utf-8')


product_df = pd.read_csv('product_info_whole.csv',index_col = 0)
ind_review_df = review_details.get_reviews(product_df)

#ind_review_df = ind_review_df[ind_review_df.user_id.notnull()]
ind_review_df.to_csv('ind_review_whole.csv',encoding='utf-8')'''
