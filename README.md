# Serverless Event Logger

## Deployed API details

Base URL: https://n32684zyrl.execute-api.ap-southeast-2.amazonaws.com/dev

### Example curl commands

#### Creating an event
```
curl -X POST -H "Content-Type: application/json" -d "{\"id\": \"1\", \"type\": \"string\", \"payload\": { \"key1\": \"value1\" }}" https://n32684zyrl.execute-api.ap-southeast-2.amazonaws.com/dev/events
```

#### Retrieving a specific event by ID
```
curl https://n32684zyrl.execute-api.ap-southeast-2.amazonaws.com/dev/events/1
```


## Setting up local virtual environment
1. Install Python 3.13. Option to manage Python versions using `pyenv`.
2. Install `uv` via `pip install uv` if not yet done.
3. Create virtual environment: `uv venv .venv`.
4. Activate venv: `.venv\Scripts\activate`.
5. Install dependencies: `uv sync`.
6. To add dependencies, execute `uv add <package_name>`. If dependency is optional, add `--group dev`.

### Running linter
```
ruff check .
```

### Running formatter
```
ruff format
```

### Running unit tests
```
pytest tests
```

### Running FastAPI app
1. Set value for environment variable `EVENTS_TABLE`.
2. Execute `uvicorn main:app --reload`.

### Deploying application to AWS
1. Install CDK: `npm install -g aws-cdk`.
2. Setup AWS credentials.
3. Activate virtual environment.
4. Change current directory to infrastructure: `cd infrastructure`.
5. If not yet done, bootstrap CDK: `cdk bootstrap aws://<AWS_ACCOUNT_ID>/<AWS_REGION>`.
6. Set environment variables: `PROJECT`, `STAGE`, `AWS_REGION`.
7. Run `cdk synth` to synthesize CloudFormation templates.
8. Run `cdk diff` to check differences between current templates and deployed stacks.
9. Run `cdk deploy --all` to deploy AWS resources.


## CI/CD

### Running the pipeline
1. Pushing to any branch will trigger the pipeline to execute lint and test.
2. Creating a pull request will also trigger the pipeline to execute lint and test.
3. Pushing to `main` branch will trigger execution of lint, test, and deployment to AWS.


## Solution design and considerations
Before scaffolding the project and creating the endpoints, I first created a [simple AWS architecture diagram](docs/serverless_event_logger.png).

I only deployed resources that are part of the free tier: API Gateway, Lambda, DynamoDB (with AWS-managed KMS key), Cloudwatch logs. But I included Route53 and WAF in the diagram because I believe they are necessary if the application will be deployed in production.

Given limited time, I focused on using technologies that I am already familiar with: Python and FastAPI. Also, I used AWS CDK's `aws_lambda_python_alpha` for simplicity in setup. However, as it is an alpha version, I do not recommend pushing this up to production.


## Workflow

### Tasks
Before starting the exercise, I listed the following as the minimum tasks needed to meet the requirements:

[x] Create public Github repository <br>
[x] Create AWS architecture diagram (via drawio) <br>
[x] Scaffold project's folder structure <br>
[x] Setup venv + initial dependencies using uv (fastapi, mangum, dyntastic, uvicorn, ruff, pytest, moto) <br>
[x] Setup Github actions (dependency installation + lint + unit test) <br>
[x] Create tests for create event endpoint <br>
[x] Implement create event endpoint <br>
[x] Create tests for get event endpoint <br>
[x] Implement get event endpoint <br>
[x] Create CDK app <br>
[x] Add deployment step in pipeline <br>
[x] Perform integration testing (via Thunder Client extension in VS Code) <br>
[x] Update readme

### Next steps if I had more time
At the 2-hour mark, I have finished scaffolding the project, setting up Github action job for lint and test, and creating the endpoints including their corresponding tests. I spent ~1.5 hours more to improve the pipeline and support deployment to AWS.

If I had more time, I would have done the following:
- Adding mypy in the pipeline for type checking
- Adding dependency caching to increase pipeline efficiency
- Making `uv` work in the pipeline (I had to install packages using pip in the end...)
- Setting env vars in a different way, instead of hardcoding in the pipeline template (e.g., create a shell script that will set the correct env vars depending on the branch)
- Setting up tox to run linter, formatter, and tests using a single command `tox`
- Setting up a local DynamoDB (via Docker) to allow full local development
- Use another branch for `dev`. Treat `main` as production branch, so only stable code should be pushed. Debugging should be done in `dev` or feature branches.

### Issues encountered
Most of the difficulties I encountered are related to the pipeline.

- I had some trouble with my setup and permissions so I cannot push my changes to the pipeline yml via Git; I had to modify it via browser only.
- I would like to use `uv` instead of `pip` when installing dependencies in the pipeline because `uv` has better performance. Unfortunately, I had difficulties in making it work. To not spend a lot more time on it, I went with the workaround of using pip when installing dependencies required to proceed with the deployment.
- It is my first time setting up Github Actions. I had some few hiccups related to syntax and setting up OIDC for AWS deployment.

### Parts of the code influenced by AI
As I am not familiar with Github Actions, I had to consult ChatGPT to help me in writing the pipeline template and setting up the necessary roles to allow CDK deployment to AWS.

In the end, I realized that the basic concepts are pretty much similar to what I have already done in Azure DevOps pipelines. They just differ mostly in syntax.


## Remaining items to be production-ready

In my opinion, the following should be done prior to production release:

- Increase security at infrastructure level by:
    - Adding API Gateway authorization (e.g., Cognito, custom lambda authorizer)
    - Enabling API Gateway rate limiting to avoid increasing costs (due to multiple Lambda invocations) and throttling of DynamoDB
    - Attaching WAF to API Gateway for added protection against common web attacks
- Using a custom domain name instead of the default API Gateway URL for stability (i.e., even when the API GW is recreated/migrated, the clients using the domain name will not be affected)
- Using customer-managed KMS key in DynamoDB to have better control over encryption
- Improve logging strategy for easier debugging
    - Format in JSON for easier querying in Cloudwatch
    - Use a logging library (e.g., loglib) instead of print() to support structured and level-based logging
- Enable Cloudwatch alarms for monitoring of errors (e.g., throttling)
- Wait for the stable and official version of `aws_lambda_python_alpha` or update the stack to use `aws_lambda`.
