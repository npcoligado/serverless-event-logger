import os

from aws_cdk import App, Tags

from stacks.database import DatabaseStack


app = App()

database_stack = DatabaseStack(
    app, f"{os.environ['PROJECT']}-{os.environ['STAGE']}-database"
)

Tags.of(app).add("PROJECT", os.environ["PROJECT"])
Tags.of(app).add("STAGE", os.environ["STAGE"])

app.synth()
