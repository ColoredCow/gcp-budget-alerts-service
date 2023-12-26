# gcp-budget-alerts-service
The micro-service is for tracking and monitoring the spending amount at the GCP service. This micro-service elevates an alert whenever the overall budget surpasses or meets predefined thresholds.

## Architecture

![_                                          Expected architecture for the Alert service](https://github.com/Sachinbisht27/gcp-budget-alerts-service/assets/96137915/86e87e12-824a-46a9-ba95-07edca694285)
<h6 align="center">Architecture for the Alert Service</h6>


## Installation Guideline

### Prerequisite
1. pyenv
2. python 3.8
3. A Slack App for delivering messages on the channel.

### Steps
1. Clone the repository
    ```sh
    git clone https://github.com/Sachinbisht27/gcp-budget-alerts-service.git
    ```
2. Switch to project folder and setup the vertual environment
    ```sh
    cd gcp-alerts
    python -m venv venv
    ```
3. Activate the virtual environment
    ```sh
    source ./venv/bin/activate
    ```
4. Install the dependencies:
    ```sh
    pip install -r requirements-dev.txt
    ```
5. Set up your .env file by copying .env.example
    ```sh
    cp .env.example .env
    ```
6. Add/update variables in your `.env` file for your environment.
7. Run the following command to get started with pre-commit
    ```sh
    pre-commit install
    ```
8. Start the server by following command
    ```sh
    functions_framework --target=handle --debug
    ```
