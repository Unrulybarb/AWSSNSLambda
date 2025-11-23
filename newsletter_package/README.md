AWS NEWSLETTER SUBSCRIPTION APP – FULL SETUP NOTES
1. Create SNS Topic

Go to SNS → Topics → Create topic

Type: Standard

Name: NewsletterTopic

Click Create

Copy the Topic ARN, e.g.:

arn:aws:sns:us-east-1:123456789012:NewsletterTopic

2. Create IAM Role for Lambda

Go to IAM → Roles → Create role

Select: AWS Service → Lambda

Attach these policies:

AmazonSNSFullAccess (or a custom sns:Subscribe policy)

AWSLambdaBasicExecutionRole

Name it: LambdaSNSRole

Create role

3. Create Lambda Function

Go to Lambda → Create function

Name: NewsletterSubscriptionLambda

Runtime: Python 3.11

Use the role: LambdaSNSRole

Paste this code (with CORS included):



Click Deploy

4. Create REST API in API Gateway
4.1 Create REST API

Go to API Gateway → Create API → REST API → Build

API name: NewsletterRESTAPI

Endpoint: Regional

Create

4.2 Create Resource

Click Actions → Create Resource

Name: subscribe

Path: /subscribe

4.3 Create POST Method

Click /subscribe → Actions → Create Method

Select: POST

Integration Type: Lambda Function

Check: Use Lambda Proxy Integration

Choose your Lambda: NewsletterSubscriptionLambda

Save

4.4 Enable CORS

Select /subscribe

Actions → Enable CORS

Allow:

Origin: *

Methods: POST, OPTIONS

Headers: Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token

Click: Enable CORS and replace existing values

4.5 Deploy API

Actions → Deploy API

Stage name: PRUD (or whatever you used)

Copy your full invoke URL:

https://6ve928xiqi.execute-api.us-east-1.amazonaws.com/PRUD/subscribe

5. Test API in Postman

Open Postman

Method: POST

URL:

https://6ve928xiqi.execute-api.us-east-1.amazonaws.com/PRUD/subscribe


Headers tab:

Content-Type: application/json

Body → raw → JSON:

{
  "email": "your-email@example.com"
}


Click Send

If everything is correct:

You will get:

{
  "message": "Subscription request sent"
}


Then SNS will email a confirmation link.

6. Common Error Fix
“Missing Authentication Token”

Means:

wrong method OR

wrong URL (missing /subscribe) OR

wrong stage name OR

trailing slash mismatch

Use the full correct URL:

.../PRUD/subscribe

“InvalidParameter: Invalid Topic Name”

Means your Lambda has:

TOPIC_ARN = "NewsletterTopic"


Instead of the full ARN.

You must set:

TOPIC_ARN = "arn:aws:sns:REGION:ACCOUNT_ID:NewsletterTopic"

7. HTML Frontend

Create index.html:

8. Complete App Flow

User enters email in the HTML form

API Gateway REST endpoint /subscribe receives POST request

API triggers Lambda

Lambda subscribes email to SNS

SNS sends confirmation email

After confirming, user is subscribed
