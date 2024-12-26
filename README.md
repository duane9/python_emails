Have Python 3.8 and pip installed
Have a program with zip functionality installed
Have Terraform installed
Have AWS CLI installed and configured. Your CLI user needs the right permissions to deploy the resources

Go to the terraform.tfvars.example file, fill out its values, and save as terraform.tfvars

From the root of this project, run setup.sh or run the steps in the file seperately

Then, go throught the terraform workflow:
terraform init
terraform plan
terraform apply