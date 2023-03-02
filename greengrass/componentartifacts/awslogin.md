1 time saml2aws configure with:

```
url                  = https://sbphnk.okta-emea.com/home/amazon_aws/0oa2zg46rqqplUlaW0i7/272
username             = <your email address used in Okta>
provider             = Okta
mfa                  = PUSH
skip_verify          = false
aws_session_duration = 43200
aws_profile          = ValueTeamRole
password = <YOUR OKTA PASSWORD>
```

awslogin() {
    saml2aws login --role arn:aws:iam::262345918484:role/ValueTeamRole --force --skip-prompt --profile cb-temporary-login --quiet --cache-saml
    export AWS_OKTA_PROFILE=nlstgoc-dev-workloads
    export AWS_REGION=eu-west-1
    export AWS_DEFAULT_REGION=eu-west-1
    eval $(saml2aws script --shell=bash --profile cb-temporary-login)
}
run `awslogin` to store temporary aws credentials in terminal