# examples

## Usage

Get your Slack legacy token from https://api.slack.com/custom-integrations/legacy-tokens.

Then, execute the following commands.

```sh
export SLACK_TOKEN=<Your token>
export SLACK_CHANNEL=<Channel to notify>
pip install -r requirements.txt -e ../
python train_mnist.py
```

You will see a warning message is shown after a while, then a message will be sent to the Slack channel which you specified, and finally the training process will exit automatically.
