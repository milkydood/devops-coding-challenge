DevOps Coding Test
==================

# The Task

You are required to provision and deploy a new service in AWS. It must:

* Be publicly accessible, but *only* on port 80.
* Return the current time on `/now`.

# Mandatory Work

Fork this repository.

* Script your service using CloudFormation, and your server configuration management tool of choice should you need one.
* Provision the service in your AWS account.
* Write a healthcheck script in Python that can be run externally to periodically check if the service is up and its clock is not desynchronised by more than 1 second.
* Alter the README to contain instructions required to:
  * Provision the service.
  * Run the healthcheck script.
* Provide us IAM credentials to login to the AWS account. If you have other resources in it make sure we can only access what is related to this test.

Once done, give us access to your fork. Feel free to ask questions as you go if anything is unclear, confusing, or just plain missing.

# Extra Credit

We know time is precious, we won't mark you down for not doing the extra credits, but if you want to give them a go...

* Run the service inside a Docker container.
* Make it highly available.

# The Submitted solution

#### Spinning up the service

After configuring credentials via `aws configure` or exporting them as environment variables, start the service:

```aws cloudformation create-stack --stack-name webtoo --template-body file://web.yaml --parameters file://webparam.json```

This will create a new cloudformation stack, with an AWS Linux t2.nano instance running the service.

You can either use this service by hitting the instance's public IP, or by hitting the ELB end-point.

#### TODO/Improvements

This can be considered a WIP. In particular, I haven't quite met this requirement:
* Write a healthcheck script in Python that can be run externally to periodically check if the service is up and its clock is not desynchronised by more than 1 second.
- In fact, I've made this healtcheck an integral part of the service, and it's being used to determine if the service is healthy. While this may be a posotive thing, it isn't what was required

* Turn off public :80 on the instances
  - have these served via the LB only

* Finish the dns part of the service
  - I've delegated part of my personal domain, test.milky.org.uk, which is a hosted AWS zone. Finish writing the ELB DNS name as a Alias in route53 via cloudformation

* Improve the python
  - It's deliberately. Seemed like a good idea at the time, to ensure it blocked checking ntp drift, but this is actually not ideal at all. It does seem like a good idea to have the healtcheck and actual service as one running process, but it should not block.

* Docker, or maybe lambda the service
  - No need for this to run on instances to manage, so fargate or lambda would be suitable candidates (bearing in mind the cost of high request lambda hits)

* Use more paremeters / cfn stacks
  - There's hardcoded values (ie subnets come to mind) in the cloudformation. This shouldn't be the case.
