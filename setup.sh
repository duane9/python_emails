#!/bin/bash

mkdir -p package
pip install boto3 openai --only-binary=:all: --upgrade --platform manylinux2014_x86_64 --target ./package --implementation cp --python-version 3.13
cd package
zip -r ../deployment_package.zip .
cd ..
zip deployment_package.zip lambda_function.py
echo "Deployment package created successfully: deployment_package.zip"
