import csv
import os
import shutil
import xml.etree.ElementTree as ET

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    train_val_path = "/home/alex/DATASETS/TODO/Amur Tiger/atrw_detection_train/trainval"
    test_path = "/home/alex/DATASETS/TODO/Amur Tiger/atrw_detection_test/test"

    boxes_path = "/home/alex/DATASETS/TODO/Amur Tiger/atrw_anno_detection_train/Annotations"

    split_path_train = (
        "/home/alex/DATASETS/TODO/Amur Tiger/atrw_anno_detection_train/ImageSets/Main/train.txt"
    )
    split_path_val = (
        "/home/alex/DATASETS/TODO/Amur Tiger/atrw_anno_detection_train/ImageSets/Main/val.txt"
    )

    train_reid_path = "/home/alex/DATASETS/TODO/Amur Tiger/atrw_reid_train/train"
    test_reid_path = "/home/alex/DATASETS/TODO/Amur Tiger/atrw_reid_test/test"

    train_reid_ann_path = (
        "/home/alex/DATASETS/TODO/Amur Tiger/atrw_anno_reid_train/reid_list_train.csv"
    )
    test_reid_ann_path = (
        "/home/alex/DATASETS/TODO/Amur Tiger/atrw_anno_reid_test/reid_list_test.csv"
    )

    ds_name_to_reid = {"train": train_reid_path, "test": test_reid_path}

    batch_size = 30

    ds_name_to_data = {
        "train": (split_path_train, train_reid_ann_path),
        "val": (split_path_val, None),
        "test": (None, test_reid_ann_path),
    }

    def create_ann_re(image_path):
        tags = [re]

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        if ds_name != "test":
            id_value = name_to_id.get(get_file_name_with_ext(image_path))
            if id_value is not None:
                id_tag = sly.Tag(id_meta, value=id_value)
                tags.append(id_tag)

        return sly.Annotation(img_size=(img_height, img_wight), img_tags=tags)

    def create_ann(image_path):
        labels = []

        ann_path = os.path.join(boxes_path, get_file_name(image_path) + ".xml")

        if file_exists(ann_path):
            tree = ET.parse(ann_path)
            root = tree.getroot()

            img_height = int(root.find(".//height").text)
            img_wight = int(root.find(".//width").text)

            all_objects = root.findall(".//object")

            for curr_object in all_objects:
                coords_xml = curr_object.findall(".//bndbox")
                for curr_coord in coords_xml:
                    left = float(curr_coord[0].text)
                    top = float(curr_coord[1].text)
                    right = float(curr_coord[2].text)
                    bottom = float(curr_coord[3].text)

                    rect = sly.Rectangle(
                        left=int(left), top=int(top), right=int(right), bottom=int(bottom)
                    )
                    label = sly.Label(rect, obj_class)
                    labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    obj_class = sly.ObjClass("tiger", sly.Rectangle, color=(255, 0, 0))
    re_meta = sly.TagMeta("re identification", sly.TagValueType.NONE)
    id_meta = sly.TagMeta("id", sly.TagValueType.ANY_NUMBER)

    re = sly.Tag(re_meta)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=[re_meta, id_meta])
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, ds_data in ds_name_to_data.items():

        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        split_path, reid_ann_path = ds_data

        if split_path is not None:
            with open(split_path) as f:
                content = f.read().split("\n")

            images_names = [im_name + ".jpg" for im_name in content if len(im_name) > 1]
            images_path = train_val_path

        else:
            images_names = images_names = [
                im_name for im_name in os.listdir(test_path) if get_file_ext(im_name) == ".jpg"
            ]
            images_path = test_path

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [
                os.path.join(images_path, image_name) for image_name in images_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            if ds_name != "test":
                anns = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

        if reid_ann_path is not None and ds_name != "test":
            name_to_id = {}
            with open(reid_ann_path, "r") as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    name_to_id[row[1]] = int(row[0])

            images_path = ds_name_to_reid[ds_name]
            images_names = [
                im_name for im_name in os.listdir(images_path) if get_file_ext(im_name) == ".jpg"
            ]

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                img_pathes_batch = [
                    os.path.join(images_path, image_name) for image_name in images_names_batch
                ]

                img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                anns = [create_ann_re(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(images_names_batch))

    return project
