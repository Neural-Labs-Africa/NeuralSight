from collections import namedtuple
from typing import Any
from app.inf.pred import predict

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, responses
from app import models, crud

from app.api import deps


router = APIRouter()


@router.post("/")
def get_covid_predictions(
    patient_id: str,
    conf_thresh: float = 0.4,
    iou_thresh: float = 0.4,
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload image and get prediction
    """
    if crud.user.is_active(current_user):
        thres = namedtuple("thres", ["conf_thres", "iou_thres"])
        inf_list, crops, results = predict(
            thres(conf_thres=conf_thresh, iou_thres=iou_thresh),
            bytes=file,
            patient_id=patient_id,
            covid=True,
        )
        # pylint: disable=R1718
        pathogens = set([str(cname).split("/")[3] for cname in crops])
        res_str = {
            "no_pathogens": len(pathogens),
            "pathogen_names": list(pathogens),
            "image_crops": crops,
            "results": results,
            "file_response": responses.FileResponse(
                inf_list[0], filename=inf_list[1].split(".")[0] + ".jpg"
            ),
        }

        return res_str

    raise HTTPException(
        status_code=400,
        detail="The user with this username isn't active.",
    )
