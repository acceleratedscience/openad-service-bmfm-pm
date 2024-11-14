# bmfm_mammal_inference

Dev note:

Testing during development:

POST to http://0.0.0.0:8080/service

This input to dti:
```json
{
    "service_type": "get_protein_property",
    "service_name": "get protein dti",
    "parameters": {
        "property_type": [
            "dti"
        ],
        "subjects": [
          "NLMKRCTRGFRKLGKCTTLEEEKCKTLYPRGQCTCSDSKMNTHSCDCKSC"
        ],
			  "drug_smiles": "'CC(=O)NCCC1=CNc2c1cc(OC)cc2'"
    }
}
```

Returns this dti value:
```json
[
	{
		"subject": "NLMKRCTRGFRKLGKCTTLEEEKCKTLYPRGQCTCSDSKMNTHSCDCKSC",
		"property": "dti",
		"result": 4.042873859405518
	}
]
```

This sol input:
```json
{
    "service_type": "get_protein_property",
    "service_name": "get protein sol",
    "parameters": {
        "property_type": [
            "sol"
        ],
        "subjects": [
          "NLMKRCTRGFRKLGKCTTLEEEKCKTLYPRGQCTCSDSKMNTHSCDCKSC"
        ]
    }
}
```

... returns this sol output:
```json
[
	{
		"subject": "NLMKRCTRGFRKLGKCTTLEEEKCKTLYPRGQCTCSDSKMNTHSCDCKSC",
		"property": "sol",
		"result": 1
	}
]
```

`params.json` is required for dti to work properly, and must be copied into
the same bucket (eventually local directory) as the dti model artifacts
downloaded from https://huggingface.co/ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd :

```json
{
    "norm_y_mean": 5.79384684128215,
    "norm_y_std": 1.33808027428196,
}
```

It is currently (and must be) uploaded into place by an admin with write access
to s3://ad-prod-biomed :

```sh
aws s3 cp params.json s3://ad-prod-biomed/molecules/mammal/dti/v0/
```
