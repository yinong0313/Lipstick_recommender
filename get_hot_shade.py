from collections import Counter

product_df = pd.read_csv('product_info_whole.csv',dtype={'loves':int})
product_df  = product_df.drop(product_df.columns[[0]], axis=1)


hot_shades_dict = Counter()
for i in product_df.index:
    print(i)
    link3 = 'https://api.bazaarvoice.com/data/reviews.json?Filter=ProductId%3A' +\
              product_df.p_id[i] + '&Sort=Helpfulness%3Adesc&Limit=' +'{}&Offset={}&Include=Products%2CComments&'.format(min(int(product_df.total_reviews[1]), int(100)), 0) +\
          'Stats=Reviews&passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4'
    print(link3)
    with urllib.request.urlopen(link3) as url:
        hot_shade_dict.clear()
        data = json.loads(url.read().decode())
        shades_name_list = product_df['shades_names'].values.tolist()[i]
        shades_name_clean = shades_name_list[2:-3].replace("\'",'').split(',')
        #print(shades_name_clean)
        for shade in shades_name_clean:
            ind_shade = shade.strip()
            for j in range(len(data['Results'])):
                if any(key_word in data['Results'][j]['ReviewText'] for key_word in ind_shade):
                    hot_shade_dict[ind_shade] +=1
        hot_shade_temp = sorted(hot_shade_dict.items(), key=lambda t: (-t[1],t[0]))
        print([hot_shade[0] for hot_shade in hot_shade_temp[0:3]])
        hot_shade_final = [hot_shade[0] for hot_shade in hot_shade_temp[0:3]]
    product_df.at[i,'hot_shade'] =hot_shade_final
product_df.loc[product_df.hot_shade.str.len() == 0,'hot_shade'] = ['N/A']
product_df.to_csv('product_info_whole.csv', encoding='utf-8')
