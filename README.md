# BMFM MAMMAL Inference for Proteins

About:
This inference Open Source Repository us based on the Bio-med Multialignment Foundation Model and provides examples of a number of Property Generation endpoints.
More Information on the model is available here:
https://github.com/BiomedSciAI/biomed-multi-alignment

The Properties it supports are 
 [ BACE, BBBP, CLINTOX, ESOL, FREESOLV, HIV, LIPOPHILICITY, MUV, QM7, SIDER, TOX21, TOXCAST ]
## Deployment Options


### Deplyoing with Sky Pilot
1 Support for skypilot on AWS is available. you must have a valid aws account setup with appropriate accound settings to allow sky pilot

 In openad running the following
Step 1:
`catalog model service from 'git@github.com:acceleratedscience/bmfm_mammal_inference.git' as mammal`
Step 2: 
`model service up mammal`

to stop the service run `model service down` in openad.

you will now have to wait until the service is available use `sky status` to see if the service is up and provisioned


### Deploying on podman / docker 
run on the command line `mkdir -p ~/.openad_models`

then using Podman or Docker run the following in the same directory as the compose.yaml file:
step 1:
`compose create`
step 2:
`compose start`

the service will start on poert `8080` change this in the compose file if you wish it to run on another port.

In openad run the following command
`catalog model service from remote 'http://127.0.0.1:8080/' as mammal`

### Deploying in venv

to deploy simply run `pip install .` the run `python ./implementation.py`


In openad run the following command once the container is up and running
`catalog model service from remote 'http://127.0.0.1:8080/' as mammal`
