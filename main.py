from reading_data import product_category,product_details,product_offer
from resource import credentials
from s3_session import load_into_s3

def main():
    prod= product_category()
    prod_details = product_details()
    prod_offer = product_offer()
    print('All the data have been loaded and ready to upload in bucket')
    for file_name in credentials.file_names:
        print(f'Loaded the data adding into the {credentials.bucket}/{file_name}')
        if file_name == 'raw/product-by-category.json':
            load_into_s3(credentials.bucket,file_name,prod)
            print(f'Data loaded into the s3 {file_name}')
        elif file_name =='raw/product-detail.json':
            load_into_s3(credentials.bucket,file_name,prod_details )
            print(f'Data loaded into the s3 {file_name}')
        else:
            load_into_s3(credentials.bucket,file_name,prod_offer)
            print(f'Data loaded into the s3 {file_name}')

if __name__ =='__main__':
    main()

