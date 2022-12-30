COPY our_staging_table
FROM '{{params.location}}'
credentials 'aws_access_key_id={{params.login}};aws_secret_access_key={{params.secret}}'
csv
IGNOREHEADER 1;