# Models on Cloud
A framework for making ML model enabled spreadsheets (Excel/Google Sheets) in minutes.

## Features
- **End-User Friendly** - no extra learning or setup needed for end users to use ML models. The deliverables run in their most familiar apps.
- **Cross Platform Support** - supercharged spreadsheets works on both Windows and macOS.
- **Pre-Built CD Pipeline** - update your model in production with one single push.
- **Opinionated Project Structure** - a clear project structure for easy collaboration.
- **Cost Efficient** - use it with no cost or minimum cost (more on this see [cost estimation section](#cost-estimation)).


## Getting Started
### Environment Setup
#### Windows
1. Clone this repo, run PowerShell as Administrator and open its location
2. Run `iex setup\windows.ps1` in PowerShell. This is going to
   install [chocolatey](https://chocolatey.org/), [AWS CLI](https://aws.amazon.com/cli/), [AWS SAM](https://aws.amazon.com/serverless/sam/),
   and [Docker Desktop](https://www.docker.com/products/docker-desktop/)
3. Reboot your computer when finished
#### macOS/Linux
1. Install AWS CLI from [here](https://aws.amazon.com/cli/)
2. Install AWS SAM
   from [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
3. Install Docker from [here](https://www.docker.com/get-started)
4. Reboot your computer when finished

### Configure AWS Account
1. Have a AWS account ready
   and [get the Access Key](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys).
   The best practice is to create
   an [IAM user account](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/users) for it
2. Run `aws configure` in your terminal of choice (could be PowerShell on Windows), and when prompted, input:
   - `AWS Access Key ID`: the AWS Access Key ID for the IAM user you created
   - `AWS Secret Access Key`: the AWS Access Key Secret for the IAM user you created
   - `Default region name`: `us-east-1`
   - `Default output format`: `json`

### First Time Deploy
1. Develop your model in `model/train.ipynb` and use the last cell to save the model object as `model.pkl`. The model
   object needs to implement `run_predict` method and `input_columns` attribute, as specified
   by `cloud_function/interfaces.py/Model` class
2. Move your model file to `cloud_function` folder
3. Add your python dependencies to `cloud_function/requirements.txt`. If you have any system dependencies, add them to
   `cloud_function/Dockerfile` (line 43). For example, if you want to use LightGBM, you need to add `libgomp` here
4. Start Docker Desktop if haven't, and run `sam build` in terminal at project root to build the project. You can then
   locally test it with `sam local start-api` command
5. Run `sam deploy --guided` in terminal at project root to deploy the project to AWS. You will be asked to provide a
   stack name (set to whatever you want) and AWS region (by default use `us-east-1`). You can use the default values for
   other options. When asked
   for `Save arguments to configuration file`, answer yes to generate a `samconfig.toml` file at root. Commit that toml
   file and push to your repo
6. Get the API endpoint from the output printed in terminal. It will be something like
   `https://<random_string>.execute-api.<region>.amazonaws.com/Prod/`

### Use the Delivery Files
#### Excel
1. Open `deliverables/excel.xlsm` in Excel.
2. Paste the API endpoint you got from deployment into sheet `Config` cell `C2`.
3. Put your input data in `INPUT_TABLE` table in sheet `Input`. Column names need to be exactly the same as what the
   model takes.
4. Find `Queries & Connections` button at `Data` tab and click it. This will open the side panel.
5. Right click `Query Prediction API` and click `Load To...` to load the result. Usually you want to create a table for the output.
#### Google Sheets
1. Find the template
   at [Google Sheets](https://docs.google.com/spreadsheets/d/1NeRJ3--OYfLClzsXZcnImhsCsjQY_dFPv1DQiAgTo-s/edit?usp=sharing)
   and make a copy of it.
2. Paste the API endpoint you got from deployment into sheet `Config` cell `C2`.
3. Put your input data in `Input` sheet starting from `A1`, including column names as the first row. Column names need
   to be exactly the same as what the model takes.
4. Click the blue `UPDATE` button at either `Input` or `Output` sheet.
5. The result will be loaded to `Output` sheet, starting from `A1`.


## Update Model After Deployment
1. Create a repo or folk this repo on GitHub, go to repo - Settings - Secrets - Actions, use `New repository secret` button to add your
   AWS access id and key as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. ![Secrets Setting](docs/secrets.jpg)
2. Change the branch name at line 4 of `./github/workflows/sam-pipeline.yaml` to your production branch name. Usually
   this is `master` or `main`, and sometimes people use `develop` as production branch as well.
3. Use `model/train.ipynb` to train the new model, use the last cell to dump the new model file, replace the old model
   file in `predict` with the new one.
4. Make sure `samconfig.toml` file from the initial deployment exists at project root, commit and push everything to the
   production branch on GitHub, it will be deployed to AWS automatically.


## Cost Estimation
Although it is possible to use this project with no cost, there are three places where AWS billing might be involved. To
begin with, every new AWS account comes 12 month of free tier benefit, which allows you to use AWS services without any
cost for certain amount of usage.

| AWS Service                      | Used For                                         | Free Tier Limit                             | Cost beyond Free Tier                                              |
|----------------------------------|--------------------------------------------------|---------------------------------------------|--------------------------------------------------------------------|
| Lambda Function                  | Provide runtime to run the container             | 1,000,000 requests per month                | [Lambda Pricing](https://aws.amazon.com/lambda/pricing/)           |
| Elastic Container Registry (ECR) | Store the Docker Image                           | 500 MB-month of Storage as private registry | [ECR Pricing](https://aws.amazon.com/ecr/pricing/)                 |
| API Gateway                      | Provide API Endpoint to access from the internet | 1,000,000 API calls received per month      | [API Gateway Pricing](https://aws.amazon.com/api-gateway/pricing/) |

If cost ever occurs, it mostly likely comes from ECR. Although this project has already adopted
serval methods to reduce image size, such as using
a [custom Lambda container image](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-create-from-alt)
and multi-stage build, but if you need to include a bunch of large dependencies, the 500MB of storage provided by the
free tier is not enough in some cases. 

Luckily, ECR cost beyond free tier is pretty reasonable. Storage is $0.10 per GB / month for data stored in private or
public repositories, meaning even if you have a giant 1GB image, the cost is only $0.1 per month.


## Architecture
![Architecture](docs/architecture.drawio.svg)
