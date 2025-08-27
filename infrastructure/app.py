import os

from aws_cdk import App, Tags

from stacks.service import ServiceStack
from stacks.database import DatabaseStack


app = App()

database_stack = DatabaseStack(
    app, f"{os.environ['PROJECT']}-{os.environ['STAGE']}-database"
)

service_stack = ServiceStack(
    app,
    f"{os.environ['PROJECT']}-{os.environ['STAGE']}-service",
    database_stack=database_stack
)
service_stack.add_dependency(database_stack)

Tags.of(app).add("PROJECT", os.environ["PROJECT"])
Tags.of(app).add("STAGE", os.environ["STAGE"])

app.synth()
