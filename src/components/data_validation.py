import os,sys
import shutil
from src.logger import logging
from src.exception import isdException
from src.entity.config_entity import DataValidationConfig
from src.entity.artifacts_entity import DataIngestionArtifact,\
                                        DataValidationArtifact



class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        """Initialize the DataValidation object.

        Args:
            data_ingestion_artifact (DataIngestionArtifact): The data ingestion artifact containing necessary information.
            data_validation_config (DataValidationConfig): The data validation configuration object.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            raise isdException(e, sys)

    def validate_all_files_exist(self) -> bool:
        """Validate the existence of all required files.

        Returns:
            bool: The validation status. True if all files exist, False otherwise.
        """
        try:
            validation_status = None

            all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)

            for file in all_files:
                if file not in self.data_validation_config.required_file_list:
                    validation_status = False
                    os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
                    with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
                    with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise isdException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        """Initiate the data validation process.

        Returns:
            DataValidationArtifact: The data validation artifact containing validation status.
        """
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            status = self.validate_all_files_exist()
            data_validation_artifact = DataValidationArtifact(
                validation_status=status)

            logging.info("Exited initiate_data_validation method of DataValidation class")
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            if status:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())

            return data_validation_artifact

        except Exception as e:
            raise isdException(e, sys)



