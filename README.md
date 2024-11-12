This project implements an ETL pipeline that fetches Amazon product data from RapidAPI, cleans and transforms it using AWS Glue, and stores the processed data in Amazon S3 in Parquet format. Docker is used for local execution of the Glue script, and the final data is processed and stored via an AWS Glue job.

Note on Credentials Management:
While the credentials were originally intended to be stored in a separate credentials.py file, I encountered an issue accessing them during the development process. As a result, I temporarily added the credentials directly into the Glue script. This is not a recommended practice for production environments. In future iterations, the credentials should be securely managed using environment variables, AWS IAM roles, or AWS Secrets Manager.

Features
Fetches raw Amazon product data from RapidAPI.
Cleans and transforms data using AWS Glue.
Stores the processed data in Amazon S3 in Parquet format:
      category: Product category information.
      details: Product details such as name, price, and description.
      delivery_info: Delivery and shipping details.
Docker is used for running the Glue script locally before execution on AWS Glue.

Technology Stack
AWS Glue for serverless ETL tasks.
Amazon S3 for storing raw and transformed data.
RapidAPI for accessing Amazon product data.
Docker for local execution of the Glue script.
Python and Boto3 for AWS interaction and API calls.
Parquet format for efficient data storage.


Steps to Execute the Code
1. Clone the Repository
2. Set Up AWS Credentials
3. Docker Setup (Optional, for Local Testing)
4. Set Up AWS Glue Job
5. Run the Glue Job
  Execute the Glue job via the AWS Glue Console. Monitor the job’s progress to ensure it runs successfully.
6. Access Processed Data

amazon-product-etl/
├── resource/                  
│   └── credentials.py         
├── src/                      
│   └── glue_script.py         
├── docker/                   
│   ├── Dockerfile             
│   └── glue_script.py         
├── main.py                    
├── s3_session.py              
├── read_data.py               
├── requirements.txt           
└── README.md                  

        
