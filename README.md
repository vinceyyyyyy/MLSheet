# Models on Cloud
A scaffold for making ML model enabled spreadsheets (Excel/Google Sheets) in minutes. Some of the features included are:
- **End-User Friendly**: no extra learning or setup needed for end users to use it, runs in their most familiar apps
- **Cross Platform Support**: supercharged spreadsheets works on both Windows and macOS
- **Pre-Built CD Pipeline**: update your model in production with one single push
- **Opinionated Project Structure**: a clear project structure for easy collaboration


## Table of Content
<!-- TOC -->
* [Models on Cloud](#models-on-cloud)
  * [Table of Content](#table-of-content)
  * [Getting Started](#getting-started)
    * [Environment Setup](#environment-setup)
      * [Windows](#windows)
      * [macOS/Linux](#macoslinux)
    * [Configure AWS Account](#configure-aws-account)
    * [First Time Deploy](#first-time-deploy)
    * [Use the Delivery Files](#use-the-delivery-files)
      * [Excel](#excel)
      * [Google Sheets](#google-sheets)
  * [Update Model After Deployment](#update-model-after-deployment)
  * [Architecture](#architecture)
<!-- TOC -->


## Getting Started
### Environment Setup
#### Windows
1. Clone this repo, run PowerShell as Administrator and open its location
2. Run `iex setup\windows.ps1` in PowerShell. This is going to
   install [chocolatey](https://chocolatey.org/), [AWS CLI](https://aws.amazon.com/cli/), [AWS SAM](https://aws.amazon.com/serverless/sam/),
   and [Docker Desktop](https://www.docker.com/products/docker-desktop/)
#### macOS/Linux
1. Install AWS CLI from [here](https://aws.amazon.com/cli/)
2. Install AWS SAM
   from [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
3. Install Docker from [here](https://www.docker.com/get-started)

### Configure AWS Account
1. Reboot your computer after the Setup finished
2. Have a AWS account ready, create
   an [IAM user account](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/users) with Access Key
3. Run `aws configure` in your terminal of choice (could be PowerShell on Windows), and when prompted, input:
   - `AWS Access Key ID`: the AWS Access Key ID for the IAM user you created
   - `AWS Secret Access Key`: the AWS Access Key Secret for the IAM user you created
   - `Default region name`: `us-east-1`
   - `Default output format`: `json`

### First Time Deploy
1. Clone this repo
2. Develop your model in `model/train.ipynb` and use the last cell to save it as `model.pkl`. The model object
   needs to implement `run_predict` method and `input_columns` attribute, as specified in `predict/interfaces.py/Model` class.
3. Move your model file to `predict/model.pkl`
4. Add your python dependencies to `predict/requirements.txt`. If you have any system dependencies, add them to
   `predict/Dockerfile` (line 43)
5. Run `sam build` in terminal at project root to build the project. You can then locally test it with `sam local start-api`
6. Run `sam deploy --guided` in terminal at project root to deploy the project to AWS. You will be asked to provide a stack name, AWS region. You
   can use the default values for other options. When asked for `Save arguments to configuration file`, answer yes to
   generate a `samconfig.toml` file at root. Commit that toml file and push to your repo
7. Get the API endpoint from the output printed in terminal. It will be something like
   `https://<random_string>.execute-api.<region>.amazonaws.com/Prod/`

### Use the Delivery Files
#### Excel
1. Open `deliverables/excel.xlsm` in Excel.
2. Paste the API endpoint you got from deployment into sheet `Config` cell `C2`.
3. Put your input data in `INPUT_TABLE` table at sheet `Input`. Column names need to be exactly the same as what the
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


## Architecture
![Architecture](docs/architecture.drawio.svg)
