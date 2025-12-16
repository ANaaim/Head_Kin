from create_model_head import model_creation_from_measured_data
from pathlib import Path
import kinematics


dict_subject_nb_point_head = {"S4" :range(13, 23),
                              "S3" :range(13,23)}

# Load the static trial
list_subjects_to_process = ["S4"]
for subject in list_subjects_to_process:
    # find in the Data folder the static trial for the subject
    folder = Path(f"Data\{subject}")
    static_files = list(folder.glob("*static*.c3d"))
    if not static_files:
        print(f"No static file found for subject {subject} in folder {folder}")
        continue
    if len(static_files) > 1:
        print(f"Multiple static files found for subject {subject} in folder {folder}, using the first one.")
    else:
        static_trial_path = static_files[0]
    print(f"Found static files for subject {subject}: {static_trial_path}")


    #static_trial_path = Path(f".\Data\static_{subject}.c3d")
    model_creation_from_measured_data(static_trial_path, model_name=f"Head_{subject}", 
                                    ind_point_to_add=dict_subject_nb_point_head[subject],
                                    animate_model=False)
    kinematics.main(f"Data/{subject}/Pdr_sa_imp-s4_39_60deg_bille.c3d", f"Head_{subject}.bioMod")
    kinematics.main(f"Data/{subject}/Pdr_sa_imp-s4_32_30deg.c3d", f"Head_{subject}.bioMod")
    kinematics.main(f"Data/{subject}/Pdr_sa_imp-s4_33_45deg.c3d", f"Head_{subject}.bioMod")
    kinematics.main(f"Data/{subject}/static_S4.c3d", f"Head_{subject}.bioMod")


