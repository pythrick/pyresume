from pyresume.db import get_database
from pyresume.pyresume import update_resume
from pyresume.github import get_github
from fastapi import APIRouter, Depends, BackgroundTasks

router = APIRouter(prefix="/v1")


@router.get("/resumes/updater")
def resume_updater(
    background_tasks: BackgroundTasks,
    db: any = Depends(get_database),
    git: any = Depends(get_github),
):
    background_tasks.add_task(update_resume, db, git)
    return
