# Newsletter Subscribe - Ready to Deploy

Files:
- lambda_function.py  : Lambda handler (Python 3.11) with CORS and SNS subscribe
- template.yaml       : AWS SAM template to create SNS topic, Lambda, and HttpApi
- subscribe.html      : Simple frontend; replace API_URL with deployed endpoint
- logo.jpeg           : Image copied from your uploaded file

## Quick deploy (SAM)

1. Install and configure AWS CLI and SAM CLI.
   - `aws configure` (provide access key, secret, region)
   - Install SAM: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

2. In this folder, run:
   ```
   sam build
   sam deploy --guided
   ```
   Accept `CAPABILITY_IAM` when prompted. At the end, SAM will print the HTTP API URL. Use that URL (append `/subscribe` if necessary) and update `subscribe.html`'s `API_URL`.

3. Alternatively, deploy resources manually via console (see template.yaml for resource names).

## Notes
- The Lambda environment variable `SNS_TOPIC_ARN` is set automatically by SAM to the created topic.
- CORS is handled in the Lambda response headers. For production, restrict `Access-Control-Allow-Origin`.
- After subscribing, recipients must confirm the subscription via the email sent by SNS.
- Replace the placeholder API URL in `subscribe.html` after deployment.