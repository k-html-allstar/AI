import os
from utils.mask_to_contour import contour
from utils.contour_utils import (
    sorted_by_contour,
    normalize_coordinates,
    change_to_map_scale,
)

# if using Apple MPS, fall back to CPU for unsupported ops
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image


def contour_extraction(image_file):

    device = torch.device("cuda")
    print(device)

    torch.autocast("cuda", dtype=torch.bfloat16).__enter__()
    # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
    if torch.cuda.get_device_properties(0).major >= 8:
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    # Load the image
    image = Image.open(image_file)
    image = np.array(image.convert("RGB"))

    # Load the model
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

    sam2_checkpoint = "../checkpoints/sam2_hiera_large.pt"
    # sam2_checkpoint = "../checkpoints/sam2_hiera_tiny.pt"
    model_cfg = "sam2_hiera_l.yaml"

    sam2_model = build_sam2(model_cfg, sam2_checkpoint, device=device)

    predictor = SAM2ImagePredictor(sam2_model)
    predictor.set_image(image)

    # Predict the mask
    input_point = np.array([[100, 100]])
    input_label = np.array([1])

    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=False,
    )

    # Convert the mask to contour
    result = contour(masks)
    c = normalize_coordinates(result)
    c = sorted_by_contour(c)
    c = change_to_map_scale(c)
