import os
from typing import Any, List, Optional
import json
from fuse.data.tokenizers.modular_tokenizer.op import ModularTokenizerOp
from fuse.data.utils.collates import CollateDefault
from mammal.examples.protein_solubility.task import ProteinSolubilityTask
from mammal.examples.dti_bindingdb_kd.task import DtiBindingdbKdTask
from mammal.keys import CLS_PRED, SCORES
from mammal.model import Mammal
from openad_service_utils import (
    DomainSubmodule,
    PredictorTypes,
    SimplePredictor,
    PropertyInfo,
)
from pydantic.v1 import Field, BaseModel


class MammalProteinSolubility(SimplePredictor):
    """MAMMAL Protein Solubility Predictor

    Classifies proteins into binary labels (based only on the protein sequence)

    The benchmark defined in paper: https://academic.oup.com/bioinformatics/article/34/15/2605/4938490 Data retrieved from: https://zenodo.org/records/1162886.

    Predicts Protein Solubility returning a binary prediction 0 = Non-Soluble 1 = Soluble -1 = Unsure.

    Example:

    <cmd> GET PROTEIN Property sol FOR \'NLMKRCTRGFRKLGKCTTLEEEKCKTLYPRGQCTCSDSKMNTHSCDCKSC\'</cmd>

    result: 1

    """

    domain: DomainSubmodule = DomainSubmodule("molecules")
    algorithm_name: str = "mammal"
    algorithm_application: str = "sol"
    algorithm_version: str = "v0"
    property_type: PredictorTypes = PredictorTypes.PROTEIN

    def setup(self):
        # Automatically infer s3 path from domain, algorithm_name,...
        # within bucket, s3://gt4sd-cos-properties-artifacts/proteins/
        finetune_output_dir = self.get_model_location()
        # setup tokenizer, load model, etc

        # load tokenizer
        # Change tokenizer_op variable to self.tokenizer_op property:
        self.tokenizer_op = ModularTokenizerOp.from_pretrained(
            os.path.join(finetune_output_dir, "tokenizer")
        )

        # Load model
        # Same with nn_model as with tokenizer_op:
        self.nn_model = Mammal.from_pretrained(
            pretrained_model_name_or_path=os.path.join(
                finetune_output_dir, "best_epoch.ckpt"
            )
        )
        self.nn_model.eval()

    def predict(self, sample: Any):
        # convert to MAMMAL style
        sample_dict = {"protein_seq": sample}
        sample_dict = ProteinSolubilityTask.data_preprocessing(
            sample_dict=sample_dict,
            protein_sequence_key="protein_seq",
            tokenizer_op=self.tokenizer_op,
        )
        print(" predicting solubility for " + str(sample))
        # converting to batch
        batch_dict = CollateDefault()([sample_dict])
        batch_dict["forward_mode"] = (
            "generate"  # forward pass in generation mode instead of teacher forcing
        )
        # arguments for transformers.generation.utils.GenerationMixin.generate()
        batch_dict["generate_kwargs"] = {
            "output_scores": True,
            "return_dict_in_generate": True,
            "max_new_tokens": 5,
        }
        # running forward
        batch_dict = self.nn_model(batch_dict)

        # process output
        ans = ProteinSolubilityTask.process_model_output(
            tokenizer_op=self.tokenizer_op,
            decoder_output=batch_dict[CLS_PRED][0],
            decoder_output_scores=batch_dict[SCORES][0],
        )

        # print prediction
        print(ans["pred"])
        return ans["pred"]


class Mammal_dti(SimplePredictor):
    """Drug–target interaction (dti) Predict the binding affinity between small-molecule drug with the target protein.

    The benchmark defined on: https://tdcommons.ai/multi_pred_tasks/dti/ This example implemented for the dataset BindingDB and the affinity expressed in Kd units.

    We also harmonize the values using data.harmonize_affinities(mode = 'max_affinity') and transforming to log-scale. We also used a Drug+Target cold-split.

    Example:

    <cmd>GET PROTEIN PROPERTY dti FOR \'NLMKRCTRGFRKLGKCTTLEEEKCKTLYPRGQCTCSDSKMNTHSCDCKSC\' USING ( drug_smiles=\'CC(=O)NCCC1=CNc2c1cc(OC)cc2\') </cmd>

    result: 4.49248

    """

    domain: DomainSubmodule = DomainSubmodule("molecules")
    algorithm_name: str = "mammal"
    algorithm_application: str = "dti"
    algorithm_version: str = "v0"
    property_type: PredictorTypes = PredictorTypes.PROTEIN
    # Target Smile definition of molecule being tested
    drug_smiles: str = Field(
        default="CC(=O)NCCC1=CNc2c1cc(OC)cc2",
        description="SMILES string definition of a drug, SMILES mst be enclosed in single quotes",
        example="'CC(=O)NCCC1=CNc2c1cc(OC)cc2'",
    )

    # norm_y_mean: float = Field(default=0.1, description="", example='0.1')
    # norm_y_std: float = Field(default=0.1, description="", example='0.1')

    def get_settings(self) -> dict:
        # get the norm _y settings that checkpoint was trained on
        try:
            print(self.get_model_location() + "/params.json")
            with open(self.get_model_location() + "/params.json") as f:
                return json.load(f)
        except Exception as e:
            print(e)
            return {}

    def setup(self):
        # Automatically infer s3 path from domain, algorithm_name,...
        # within bucket, s3://gt4sd-cos-properties-artifacts/proteins/
        finetune_output_dir = self.get_model_location()
        # setup tokenizer, load model, etc

        # load tokenizer
        # Change tokenizer_op variable to self.tokenizer_op property:
        self.tokenizer_op = ModularTokenizerOp.from_pretrained(
            os.path.join(finetune_output_dir, "tokenizer")
        )

        # Load model
        # Same with nn_model as with tokenizer_op:
        self.nn_model = Mammal.from_pretrained(
            pretrained_model_name_or_path=os.path.join(
                finetune_output_dir, "best_epoch.ckpt"
            )
        )
        self.nn_model.eval()

    def predict(self, sample: Any):
        # convert to MAMMAL style
        print("running dti query for : " + sample)
        print("target drug smiles: " + self.drug_smiles)

        # get normalised parameters
        parameters = self.get_settings()
        if not parameters:
            print("Error Model Normalised Parameters Not present in model directory")
            return "Error Model Normalised Parameters Not present in model directory"
        else:
            print(
                "paramters loaded for "
                + self.get_model_location()
                + "/best_epoch.ckpt"
                + " are: "
                + str(parameters)
            )

        sample_dict = {"target_seq": sample, "drug_seq": self.drug_smiles}
        sample_dict = DtiBindingdbKdTask.data_preprocessing(
            sample_dict=sample_dict,
            tokenizer_op=self.tokenizer_op,
            target_sequence_key="target_seq",
            drug_sequence_key="drug_seq",
            norm_y_mean=None,
            norm_y_std=None,
        )

        # converting to batch
        batch_dict = CollateDefault()([sample_dict])
        batch_dict = self.nn_model.forward_encoder_only([sample_dict])
        # process output
        batch_dict = DtiBindingdbKdTask.process_model_output(
            batch_dict,
            scalars_preds_processed_key="model.out.dti_bindingdb_kd",
            norm_y_mean=parameters["norm_y_mean"],
            norm_y_std=parameters["norm_y_std"],
        )
        ans = {
            "model.out.dti_bindingdb_kd": float(
                batch_dict["model.out.dti_bindingdb_kd"][0]
            )
        }

        # print prediction
        print("result: " + str(ans))
        return ans["model.out.dti_bindingdb_kd"]


# Registering Services

Mammal_dti.register()
MammalProteinSolubility.register()

if __name__ == "__main__":
    from openad_service_utils import start_server

    start_server(port=8080)
