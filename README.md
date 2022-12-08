# Models on Cloud
A template for empowering business users with machine learning models.

## How to Use This Template
### Setup
1. Have a AWS account ready, create an IAM user account with access key
2. Install AWS CLI from [here](https://aws.amazon.com/cli/)
3. [Configure your AWS account in AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)
4. Install AWS SAM
   from [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
5. Install Docker from [here](https://www.docker.com/get-started)

### First Time Deploy
1. Clone this repo
2. Develop your model in `/model/train.ipynb` and use the last cell to save it in `/model/model.pkl`. The model object
   needs to implement `predict` method and `input_columns` attribute, as specified in `/predict/utils.py/Model` class.
3. Move your model file to `/predict/model.pkl`
4. Add your python dependencies to `/predict/requirements.txt`. If you have any system dependencies, add them to
   `/predict/Dockerfile` (line 43)
5. Run `sam build` at root to build the project
6. Run `sam deploy --guided` at root to deploy the project. You will be asked to provide a stack name, AWS region. You
   can use the default values for other options. The deploy process will generate a `samconfig.toml` file at root.
   Commit that and push to your repo.
7. Get the API endpoint from the output of the deployment. It will be something like
   `https://<random_string>.execute-api.<region>.amazonaws.com/Prod/`
8. Copy the API endpoint and paste it in `/deliverables/delivery.xlsm` at sheet `Config` cell `C2`

### Use the Delivery File
1. Open `/deliverables/delivery.xlsm` in Excel, make sure sheet `Config` cell `C2` is filled with correct API endpoint.
2. Put your input data in `INPUT_TABLE` table at sheet `Input`. Column names need to be exactly the same as what the
   model takes.
3. Find `Queries & Connections` button at `Data` tab and click it. This will open the side panel.
4. Right click `Query Prediction API` and click `Load To...`. Usually you want to create a table for the output.

### To Update Model After Deployment, Automated with GitHub Actions
1. Create a repo on GitHub, go to repo - Settings - Secrets - Actions, use `New repository secret` button to add your
   AWS access id and key as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. ![Secrets Setting](docs/secrets.jpg)
2. Update `model/train.ipynb` to train the new model.
3. Use the last cell to dump the new model file.
4. Replace `predict/model.pkl` with the new model file.
5. Commit and push the changes to the repo, it will be deployed to AWS automatically.

## Architecture
![Architecture](docs/architecture.drawio.svg)