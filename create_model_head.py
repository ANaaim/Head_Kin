"""
This example shows how to create a personalized kinematic model from a C3D file containing a static trial.
Here, we generate a simple lower-body model with only a trunk segment.
The marker position and names are taken from Maldonado & al., 2018 (https://hal.science/hal-01841355/)
"""

import os

import numpy as np
from biobuddy import (
    Axis,
    BiomechanicalModel,
    C3dData,
    Marker,
    Mesh,
    Segment,
    SegmentCoordinateSystem,
    Translations,
    Rotations,
    DeLevaTable,
    Sex,
    SegmentName,
    ViewAs,
    SegmentCoordinateSystemUtils,
    RotoTransMatrix,
)
from pathlib import Path


def model_creation_from_measured_data(static_trial_path: Path, model_name: str, 
                                      ind_point_to_add: list,
                                      animate_model: bool = True):

    static_trial = C3dData(str(static_trial_path))
    output_model_filepath = f"{model_name}.bioMod"
    # Generate the personalized kinematic model
    reduced_model = BiomechanicalModel()
    reduced_model.add_segment(Segment(name="Ground"))

    reduced_model.add_segment(
        Segment(
            name="Thorax",
            parent_name="Ground",
            translations=Translations.XYZ,
            rotations=Rotations.XYZ,
            segment_coordinate_system=SegmentCoordinateSystem(
                origin=SegmentCoordinateSystemUtils.mean_markers(["IJ", "T1"]),
                first_axis=Axis(
                    name=Axis.Name.X,
                    start="T1",
                    end="IJ"),
                second_axis=Axis(name=Axis.Name.Y, start="T3", end="T1"),
                axis_to_keep=Axis.Name.X,
            ),
            mesh=Mesh(("IJ", "PX", "T1", "T3"), is_local=False),
        ))
    
    reduced_model.segments["Thorax"].add_marker(Marker("IJ", is_technical=True, is_anatomical=True))
    reduced_model.segments["Thorax"].add_marker(Marker("PX", is_technical=True, is_anatomical=True))
    reduced_model.segments["Thorax"].add_marker(Marker("T1", is_technical=True, is_anatomical=True))
    reduced_model.segments["Thorax"].add_marker(Marker("T2", is_technical=True, is_anatomical=True))
    reduced_model.segments["Thorax"].add_marker(Marker("T3", is_technical=True, is_anatomical=True))
    

    reduced_model.add_segment(
        Segment(
            name="Head",
            parent_name="Thorax",
            translations=Translations.XYZ,
            rotations=Rotations.ZYX,
            segment_coordinate_system=SegmentCoordinateSystem(
                origin=SegmentCoordinateSystemUtils.mean_markers(["R_ear", "L_ear"]),
                first_axis=Axis(
                    name=Axis.Name.Y,
                    start=SegmentCoordinateSystemUtils.mean_markers(["R_ear", "L_ear"]),
                    end="Up_head"),
                second_axis=Axis(name=Axis.Name.Z, start="L_ear", end="R_ear"),
                axis_to_keep=Axis.Name.Z,
            ),
            mesh=Mesh(("R_ear", "L_ear", "Occ", "Up_head", "Front_Head"), is_local=False),
        ))
    
    for ind in ind_point_to_add:
        reduced_model.segments["Head"].add_marker(Marker(f"Tech_{ind:02d}", is_technical=True, is_anatomical=True))

    # Put the model together, print it and print it to a bioMod file
    model_real = reduced_model.to_real(static_trial)
    model_real.to_biomod(output_model_filepath)

    if animate_model:
        model_real.animate(view_as=ViewAs.BIORBD, model_path=output_model_filepath)


    return model_real


# def main():

#     # Load the static trial
#     static_trial = C3dData(f".\Data\static_S4.c3d")
#     print("Creating the model from measured data...")
#     model_creation_from_measured_data(static_trial, model_name="Head_S4", ind_point_to_add=list(range(13, 23)))


if __name__ == "__main__":
    main()
