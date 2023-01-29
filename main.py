import pydicom
import csv
import os
from glob import glob

source_path = os.path.join(os.path.dirname(__file__),"src\*")


def anonymize_patient(dicom_file: pydicom.FileDataset, default_name: str = ''):
    """Anonymizing Patient's name"""
    try:
        dicom_file.PatientName = default_name
    except AttributeError:
        print(f'Problem with Patient id {dicom_file.PatientID}: "PatientName" key does not exist!\nCreating empty key...')
        dicom_file.PatientName = default_name


def get_save_path(dicom_file: pydicom.FileDataset) -> str:
    """Returns save path from dicom attributes"""
    return f'out\{dicom_file.StudyInstanceUID}\{dicom_file.SeriesInstanceUID}\\'


def get_new_filename(dicom_file: pydicom.FileDataset) -> str:
    """Returns save path from dicom attributes"""
    return f'{dicom_file.SOPInstanceUID}.dcm'


def make_dirs(dicom_file: pydicom.FileDataset):
    """Creates directories from dicom attributes"""
    try:
        os.makedirs(get_save_path(dicom_file))
    except FileExistsError:
        print(f'Directory {get_save_path(dicom_file)} already exist.')


def main(path:str):
    """main function that saves anonymized dicoms in a new place and writes locations in csv"""

    with open ('output_path.csv', 'w', encoding='UTF-8', newline='') as csv_file:
        header = ['Source', 'Output']
        writer = csv.DictWriter(csv_file, header, delimiter=';')
        writer.writeheader()
        for dicom in glob(path):
            file = pydicom.dcmread(dicom)
            full_path = get_save_path(file) + get_new_filename(file)

            anonymize_patient(file)
            make_dirs(file)

            file.save_as(full_path)
            writer.writerow({'Source': dicom, 'Output': full_path})


if __name__ == '__main__':
    main(source_path)