import http.client
from resource import credentials
import urllib.parse


conn = http.client.HTTPSConnection(credentials.api_host)
headers = {
            'x-rapidapi-key': credentials.api_key,
            'x-rapidapi-host': credentials.api_host
        }

def product_category():
    params = {
    'category_id': credentials.category_id,
    'page': credentials.page,
    'country': credentials.country,
    'sort_by': credentials.sort_by,
    'product_condition': credentials.product_condition,
    'brand': credentials.brand,
    'is_prime': credentials.prime,
    'deals_and_discounts': credentials.deals
    }
    encoded_params = urllib.parse.urlencode(params)
    url = f"/products-by-category?{encoded_params}"
    print('Getting the Product by category data')
    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def product_details():
    params = {
                'asin': credentials.asin,
                'country': credentials.country
            }


    encoded_params = urllib.parse.urlencode(params)
    url = f"/product-details?{encoded_params}"
    print('Getting the Product Details Data')

    
    conn.request("GET", url,headers=headers)
    res = conn.getresponse()
    prod_data = res.read()
    return prod_data.decode("utf-8")

def product_offer():
    params = {
            'asin': credentials.asin,
            'country': credentials.country,
            'page':credentials.page
        }
    encoded_params = urllib.parse.urlencode(params)
    url = f"/product-offers?{encoded_params}"
    print('Getting data of product_offer')
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    offer_data = res.read()
    return offer_data.decode("utf-8")