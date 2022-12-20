init_buckets:
	aws s3api create-bucket --bucket pqicomponentartifacts --region eu-west-1 --create-bucket-configuration LocationConstraint=eu-west-1

upload_inference_script:
	aws s3 sync ./componentartifacts/. s3://pqicomponentartifacts
	
create_component:
	aws greengrassv2 create-component-version --inline-recipe fileb://recipes/componentrecipe.json

create_deployment:
	aws greengrassv2 create-deployment --cli-input-json file://deployment.json

deploy: upload_files_to_s3 create_component create_deployment
	echo "Deployment done"
