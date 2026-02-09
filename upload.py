from huggingface_hub import HfApi, upload_folder

model_id = "mine0107/MKD_DS_Project1"
local_model_path = "backend/models/finetuned-merged"

api = HfApi()

# Don't call create_repo again since it already exists
# api.create_repo(repo_id=model_id, private=True, exist_ok=True)

upload_folder(
    repo_id=model_id,
    folder_path=local_model_path,
    path_in_repo=".",  # root of the repo
)