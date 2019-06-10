import pandas as pd
#from random import randint
from sklearn import base
from sklearn.feature_extraction import DictVectorizer
from sklearn.neighbors import NearestNeighbors


def bayes_sum(N, mu):
    return lambda x: (x.sum() + mu*N) / (x.count() + N)


##load csv files
def get_recommender(demo_code):

    ind_review_df = pd.read_csv('ind_review_whole.csv',dtype={'demo': str})
    product_df = pd.read_csv('product_info_whole_with_hotshade.csv',dtype={'loves':int})
    ind_review_df  = ind_review_df.drop(ind_review_df.columns[[0]], axis=1)
    product_df  = product_df.drop(product_df.columns[[0]], axis=1)

    demo_dict_temp = []
    for line in ind_review_df.itertuples():
        attri_eyecolor = line[6]
        attri_haircolor = line[7]
        attri_skintone = line[8]

        if str(line[6]) == 'nan':
            attri_eyecolor = 'NAeyecolor'
        if str(line[7]) == 'nan':
            attri_haircolor = 'NAhaircolor'
        if str(line[8]) == 'nan':
            attri_skintone = 'NAskintone'

        demo_dict_temp.append({attri_eyecolor:line[10][0],attri_haircolor:line[10][1],attri_skintone:line[10][2]})

    #find user similarity, find the NearestNeighbors
    demo_dict = pd.Series(demo_dict_temp, index = ind_review_df['user_id'])
    features = DictVectorizer().fit_transform(demo_dict)
    nn = NearestNeighbors(n_neighbors=80, metric='cosine', algorithm='brute').fit(features)
    #input user demo code
    num_user_upper = len(ind_review_df[ind_review_df.demo==str(demo_code)].index)

    if num_user_upper == 0:
        demo_code = 439
        num_user_upper = len(ind_review_df[ind_review_df.demo==str(demo_code)].index)
    #num_user = [randint(0, num_user_upper-1) for p in range(0, 10)]
    num_user = range(0,min(10,num_user_upper))

    sample_user_id = ind_review_df[ind_review_df.demo==str(demo_code)].iloc[num_user].user_id.tolist()

    #user-user
    #sample_user_index = [randint(0, len(sample_user_id)-1) for p in range(1, 2)]
    dists, indices = nn.kneighbors(features[demo_dict.index.get_loc(sample_user_id[0]), :])
    neighbors = [ind_review_df.index[i] for i in indices[0]][1:]
    ratings_grp = ind_review_df[ind_review_df.index.isin(neighbors)].groupby('product_id')['user_rating']
    recom = ratings_grp.aggregate(bayes_sum(5, 4)).sort_values(ascending=False)
    recom_df = pd.DataFrame(recom)
    recom_df = recom_df.drop(recom_df[recom_df.index=='P429916'].index)

    print(recom_df)
    product_df.loc[product_df.hot_shade.isnull(),'hot_shade'] = [' N/A ']

    avg_score_dict = ind_review_df.set_index('product_id').to_dict()['avg_score']
    img_dict = product_df.set_index('p_id').to_dict()['img']
    hot_shade_dict = product_df.set_index('p_id').to_dict()['hot_shade']

    for key in avg_score_dict:
        recom_df.loc[recom_df.index == key, 'avg_score'] = avg_score_dict[key]

    for key in img_dict:
        recom_df.loc[recom_df.index == key, 'img'] = img_dict[key]

    for key in hot_shade_dict:
        recom_df.loc[recom_df.index == key, 'hot_shade'] = hot_shade_dict[key]

    recom_df_combined = recom_df.sort_values(['avg_score'], ascending=[False])
    recom_output_temp = product_df[product_df.p_id.isin(recom_df_combined.index[0:8])]
    recom_output_temp.insert(5,'avg_score',recom_df_combined.avg_score.values[0:8])
    recom_output = recom_output_temp.loc[:,['brand_names','product_names','ratings','avg_score','loves','links2','img','hot_shade']]
    return recom_output
#recom_output = get_recommender()
