creds="$(aws sts get-session-token --serial-number $AWS_IAM_SERIAL_NUMBER --token-code $1)"

export AWS_ACCESS_KEY_ID=$(printf "%s" "$creds" | jq -r .Credentials.AccessKeyId)
export AWS_SECRET_ACCESS_KEY=$(printf "%s" "$creds" | jq -r .Credentials.SecretAccessKey)
export AWS_SESSION_TOKEN=$(printf "%s" "$creds" | jq -r .Credentials.SessionToken)

echo $AWS_ACCESS_KEY_ID
