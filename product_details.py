from scrapy.http import TextResponse
import numpy as np
import requests
import re

def product_info_layer2(links2):

    p_price = []
    num_color = []
    p_num_reviews_final = []
    p_loves = []
    name_color = []

    for link in links2:
        print(links2.index(link))
        print(link)
        response2 = requests.get(link)
        url = link
        response2 = TextResponse(body=response2.content, url=url)

        p_loves_temp = response2.xpath('//span[@data-at="product_love_count"]/text()').extract()
        p_loves.append(p_loves_temp[0])

        try:
            p_price_temp = response2.xpath('//div[@data-comp="Price Box"]/text()').extract()
            p_price.append(p_price_temp[0])
            img_text = response2.xpath('//svg[@class="css-1ixbp0l"]/image').extract()
            img_temp = re.split('href="|" onload',img_text[0])
            print('https://www.sephora.com'+ img_temp[1])
            img.append('https://www.sephora.com'+ img_temp[1])
            num_color_temp = response2.xpath('//div[@class="css-1ax77m2"]').extract()
            num_color.append(len(num_color_temp))
            name_color_temp = response2.xpath('//div[@class="css-1ax77m2"]//@aria-label').extract()
            name_color_v1= [item.replace(" - Selected",'') for item in name_color_temp]
            name_color_v2 = [item.replace("Out of stock: ",'') for item in name_color_v1]
        except:
            p_price.append(None)
            num_color.append(None)
            name_color_v2 = None
            img.append(None)
        name_color.append(name_color_v2)
        p_num_reviews = response2.xpath('//span[@class="css-2rg6q7"]/text()').extract()
        p_num_reviews = p_num_reviews[0]
        p_num_reviews = p_num_reviews.replace('s', '')
        p_num_reviews = p_num_reviews.replace(' review', '')
        if len(p_num_reviews)==2:
            if p_num_reviews[1] == 'K':
                p_num_reviews = 1000*int(p_num_reviews[0])
        elif len(p_num_reviews) >2:
            if p_num_reviews[2] == 'K':
                p_num_reviews = 10000*int(p_num_reviews[0]) + 1000*int(p_num_reviews[1])
        else:
            p_num_reviews = int(p_num_reviews)
        p_num_reviews_final.append(p_num_reviews)

        print ('Number of reviews: {}'.format(p_num_reviews))
    return p_price, num_color, p_num_reviews_final, p_loves, name_color,img
