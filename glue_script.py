import json
import boto3
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from awsglue.context import GlueContext


access_key = 'AKIAYKFQQVQXMWVFMECM'
secret_key = '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'
bucket = 'amazon-product-data1'
file_names = ['raw/product-by-category.json', 'raw/product-detail.json', 'raw/product-offer.json']


category_output_path = "s3a://amazon-product-data1/processed_data/category/"
details_output_path = "s3a://amazon-product-data1/processed_data/details/"
delivery_info_output_path = "s3a://amazon-product-data1/processed_data/delivery_info/"


sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

def get_s3_client():
    """Returns an S3 client for fetching data from S3."""
    return boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

def load_json_from_s3(file_key):
    """Load JSON data from S3 bucket."""
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=bucket, Key=file_key)
    return json.loads(response['Body'].read().decode('utf-8'))

def get_category_data():
    """Load and clean category data."""
    print('Loading category data from S3...')
    json_obj = load_json_from_s3(file_names[0])
    category = json_obj['data']['products']
    
    category_df = spark.createDataFrame(category)
    print('Category data loaded into DataFrame.')


    columns_to_drop = [
        'currency', 'product_url', 'product_photo', 'product_minimum_offer_price', 'climate_pledge_friendly',
        'has_variations', 'is_best_seller', 'is_amazon_choice', 'product_availability'
    ]
    category_df = category_df.drop(*columns_to_drop)


    category_df = category_df.withColumn(
        'product_original_price', 
        when(col('product_original_price').isNotNull(), regexp_replace('product_original_price', r'\$', '')).otherwise(0)
    )
    category_df = category_df.withColumn(
        'product_price', 
        when(col('product_price').isNotNull(), regexp_replace('product_price', r'\$', '')).otherwise(0)
    )


    category_df = category_df.withColumn(
        'product_title', regexp_extract('product_title', r'^([A-Za-z0-9 ]+)(?=,|\s*\d|$)', 0)
    )
    category_df = category_df.withColumn(
        'delivery', regexp_extract('delivery', r'(FREE delivery [A-Za-z]+, [A-Za-z]+ \d+)', 0)
    )
    
    print('Category data cleaned.')
    return category_df

def get_details_data():
    """Load product details data."""
    print('Loading product details data from S3...')
    json_details = load_json_from_s3(file_names[1])
    
    all_product_info = [record['product_information'] for record in json_details['data']]
    details_df = spark.createDataFrame(all_product_info)
    print('Product details data loaded into DataFrame.')
    
    return details_df


category_df = get_category_data()
details_df = get_details_data()


delivery_info = category_df.select('asin', 'delivery')

category_df = category_df.drop('delivery', 'fastest delivery')

matching_column = category_df.select('asin', 'product_title')
joined_df = matching_column.join(details_df, on='asin', how='inner')


joined_df.show()


try:
    print('Saving processed data to S3...')
    category_df.write.mode("overwrite").parquet(category_output_path)
    joined_df.write.mode("overwrite").parquet(details_output_path)
    delivery_info.write.mode("overwrite").parquet(delivery_info_output_path)
    print('Data saved successfully.')
except Exception as e:
    print(f"Error during data saving: {e}")

print('Processing complete.')
