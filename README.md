# BMFM MAMMAL Inference for Proteins
 <!-- omit from toc -->
[![License MIT](https://img.shields.io/github/license/acceleratedscience/openad_service_utils)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docs](https://img.shields.io/badge/website-live-brightgreen)](https://acceleratedscience.github.io/openad-docs/) <br>
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## About: <!-- omit from toc -->
the below Repository is based on the Foundation Model Biomedmultialignment and provides checkpoints for 2 properties Sol and DTI

<img src='images/mammal.png' :heigth="60%" width="60%" >


More information can be found at:<br> 
https://github.com/BiomedSciAI/biomed-multi-alignment

--- 
<br>

## Deployment Options <!-- omit from toc -->

<!-- toc -->

- [Deployment locally using a Python virtual environment](#deployment-locally-using-a-python-virtual-environment)

- [Deployment locally via container](#deployment-locally-via-container)

- [Deployment On OpenShift](#deployment-lon-openshift)

- [Deployment via Sky Pilot](#deployment-via-sky-pilot)

<!-- tocstop -->
<br>

--- 

# Deployment locally using a Python virtual environment 
<br>
you will need a python level of 3.11 & to follow the following installation directions:<br>
<br>
https://github.com/BiomedSciAI/biomed-multi-alignment
<br>

Once installed you can install the openad wrapper
git+https://github.com/acceleratedscience/openad_service_utils.git
<br>
***Note:*** <br>
- Initially downloading models may take some time, this will be prompted by your first request. To pre-load models you can run the following <br>

`mkdir -p ~/.openad_models/properties/molecules && aws s3 sync s3://ad-prod-biomed/molecules/mammal/ /tmp/.openad_models/properties/molecules/mammal --no-sign-request --exact-timestamps`

<br>
it does require installing the AWS cli which can be found here..<br>

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html


Then run `python ./implementation.py`


In OpenAD run the following command once the container is up and running
`catalog model service from remote 'http://127.0.0.1:8080/' as mammal`


# Deployment locally via container
<br>
run on the command line `mkdir -p ~/.openad_models`

***Note:*** <br>
Initially downloading models may take some time, this will be prompted by your first request. To pre-load models you can run the following <br><br>
`mkdir -p ~/.openad_models/properties/molecules && aws s3 sync s3://ad-prod-biomed/molecules/mammal/ /tmp/.openad_models/properties/molecules/mammal --no-sign-request --exact-timestamps`
<br>
it does require installing the AWS cli which can be found here..

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html

then using Podman or Docker run the following in the same directory as the compose.yaml file:
### step 1:
`(podman or docker) compose create`<br>
### step 2:
`(podman or docker) start`<br>

the service will start on poert `8080` change this in the compose file if you wish it to run on another port.
### Step 3:
In openad run the following command
`catalog model service from remote 'http://127.0.0.1:8080/' as mammal`

### Notes

- The container used is https://quay.io/ibmdpdev/bmfm_mammal_properties:latest

- You can use the compose.yaml file rather than download the entire repository

https://github.com/acceleratedscience/bmfm_mammal_inference/blob/main/compose.yaml

- This container will only run on x86 architecture currently



# Deployment On OpenShift
Helm Charts are available for OpenShift including Auto scaling of services.

See the helm-chart directory in the repository

This currently does not support aynchronous requests, you can enable it if you deploy a shared filesystem, or only have a single pod running.


# Deployment via Sky Pilot
<br>
Support for skypilot on AWS is available. you must have a valid aws account setup with appropriate accound settings to allow sky pilot

### In openad running the following at the OpenAD prompt or Magic Command
### Step 1:
`catalog model service from 'git@github.com:acceleratedscience/bmfm_mammal_inference.git' as mammal`<br>
### Step 2: 
`model service up mammal` <br>

To stop the service run `model service down mammal` in openad.

***Note*** you will now have to wait until the service is available use `sky status` to see if the service is up and provisioned

