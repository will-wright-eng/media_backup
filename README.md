# media_backup
backup large media files to S3 bucket

## Table of Contents
- [Summary](README.md#summary)
- [Resources](README.md#resources)

## Summary

Kept getting an `AccessDenied` error when attempting a `CreateMultipartUpload` as per [this post](https://stackoverflow.com/a/50118024/14343465), which should have been solved by [modifying permissions](https://stackoverflow.com/questions/52541933/accessdenied-when-calling-the-createmultipartupload-operation-in-django-using-dj) -- alas, no such luck. So I went the slow route.

In my experience the `Callback` parameter in `s3.upload_file` tends to cause more problems than it solves ([docs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html#the-callback-parameter)).

## Resources used
- [SO Post](https://stackoverflow.com/a/53826161/14343465)
- [AWS S3 Bucket Permissions](https://aws.amazon.com/premiumsupport/knowledge-center/s3-console-access-certain-bucket/)

## TODO
- add check to see if key already exists, if so then compare size of each
- add wraper that treats `aws s3` as a simple service to upload, download, search_keyword, get_status (storage tier & recovery status), and recover (from glacier)

`<bucket>`

`<keyword>`
```bash
aws s3 ls <bucket>/media_uploads/ | grep "<keyword>"
```

`<filename>`
- recovery tier = Expedited
- recovery days = 10
```bash
aws s3api restore-object --bucket <bucket> --key media_uploads/<filename> --restore-request '{"Days":10,"GlacierJobParameters":{"Tier":"Expedited"}}'

#eg
aws s3api restore-object --bucket <bucket> --key media_uploads/Harry_Potter.zip --restore-request '{"Days":10,"GlacierJobParameters":{"Tier":"Expedited"}}'
```

`<check_status>`
```bash
#eg
aws s3api head-object --bucket <bucket> --key media_uploads/<filename>
```

`<download>`
```bash
#eg
aws s3 cp s3://<bucket>/media_uploads/<filename> <filename>
```