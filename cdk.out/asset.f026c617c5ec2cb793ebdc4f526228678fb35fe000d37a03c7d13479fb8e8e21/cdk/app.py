#!/usr/bin/env python3
import aws_cdk as cdk
from stack import SurveyPlaywrightStack

app = cdk.App()
SurveyPlaywrightStack(app, "SurveyPlaywrightStack")
app.synth()