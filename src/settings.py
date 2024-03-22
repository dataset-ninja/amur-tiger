from typing import Dict, List, Literal, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "Amur Tiger"
PROJECT_NAME_FULL: str = "ATRW: Amur Tiger Re-identification in the Wild Dataset"
HIDE_DATASET = True  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_NC_SA_4_0(source_url="https://lila.science/datasets/atrw")
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Environmental()]
CATEGORY: Category = Category.Environmental()

CV_TASKS: List[CVTask] = [CVTask.ObjectDetection(), CVTask.Identification()]
ANNOTATION_TYPES: List[AnnotationType] = None

RELEASE_DATE: Optional[str] = "2020-10-31"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://cvwc2019.github.io/challenge.html"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 16240186
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/amur-tiger"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "Detection train images": "https://storage.googleapis.com/public-datasets-lila/cvwc2019/train/atrw_detection_train.tar.gz",
    "Detection test images": "https://storage.googleapis.com/public-datasets-lila/cvwc2019/test/atrw_detection_test.tar.gz",
    "Detection train annotations": "https://storage.googleapis.com/public-datasets-lila/cvwc2019/train/atrw_anno_detection_train.tar.gz",
    "Re-ID train images": "https://storage.googleapis.com/public-datasets-lila/cvwc2019/train/atrw_reid_train.tar.gz",
    "Re-ID test images": "https://storage.googleapis.com/public-datasets-lila/cvwc2019/test/atrw_reid_test.tar.gz",
    "Re-ID train annotations": "https://storage.googleapis.com/public-datasets-lila/cvwc2019/train/atrw_anno_reid_train.tar.gz",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]] or Literal["predefined"]] = {"tiger": [255, 0, 0]}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = "https://arxiv.org/pdf/1906.05586"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = None

CITATION_URL: Optional[str] = None
AUTHORS: Optional[List[str]] = ["Shuyuan Li", "Jianguo Li", "Hanlin Tang", "Rui Qian", "Weiyao Lin"]
AUTHORS_CONTACTS: Optional[List[str]] = [
    "shuyuanli@sjtu.edu.cn",
    "jglee@outlook.com",
    "hanlin.tang@intel.com",
    "qrui9911@sjtu.edu.cn",
    "wylin@sjtu.edu.cn",
]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "Shanghai Jiao Tong University, China",
    "Ant Group, China",
    "Intel Corporation, USA",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://en.sjtu.edu.cn/",
    "https://www.antgroup.com/en",
    "https://www.intel.com/",
]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "__POSTTEXT__": "Additionally, some image marked with its ***re identification*** and ***id*** tags"
}
TAGS: Optional[
    List[
        Literal[
            "multi-view",
            "synthetic",
            "simulation",
            "multi-camera",
            "multi-modal",
            "multi-object-tracking",
            "keypoints",
            "egocentric",
        ]
    ]
] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
