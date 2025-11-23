import os
import pydicom
from datetime import datetime
from .models import Patient, Study, Series, ImageInstance
from django.utils import timezone

def parse_dicom_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        return None

def parse_dicom_time(time_str):
    if not time_str:
        return None
    try:
        # Handle fractional seconds if present
        if '.' in time_str:
            time_str = time_str.split('.')[0]
        return datetime.strptime(time_str, "%H%M%S").time()
    except ValueError:
        return None

def import_study_from_folder(folder_path):
    """
    Scans a folder for DICOM files and imports them into the database.
    """
    count = 0
    errors = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Attempt to read the file as DICOM
                ds = pydicom.dcmread(file_path, stop_before_pixels=True)
                
                # Extract Patient Data
                patient_id = str(ds.get('PatientID', 'Unknown'))
                patient_name = str(ds.get('PatientName', 'Unknown'))
                patient_dob = parse_dicom_date(ds.get('PatientBirthDate'))
                patient_sex = str(ds.get('PatientSex', ''))

                patient, _ = Patient.objects.get_or_create(
                    patient_id=patient_id,
                    defaults={
                        'name': patient_name,
                        'birth_date': patient_dob,
                        'sex': patient_sex
                    }
                )

                # Extract Study Data
                study_uid = str(ds.get('StudyInstanceUID'))
                study_date = parse_dicom_date(ds.get('StudyDate'))
                study_time = parse_dicom_time(ds.get('StudyTime'))
                modality = str(ds.get('Modality', 'Unknown'))
                study_desc = str(ds.get('StudyDescription', ''))

                study, _ = Study.objects.get_or_create(
                    study_instance_uid=study_uid,
                    defaults={
                        'patient': patient,
                        'study_date': study_date,
                        'study_time': study_time,
                        'modality': modality,
                        'description': study_desc
                    }
                )

                # Extract Series Data
                series_uid = str(ds.get('SeriesInstanceUID'))
                series_desc = str(ds.get('SeriesDescription', ''))
                series_number = ds.get('SeriesNumber')
                if series_number:
                    series_number = int(series_number)

                series, _ = Series.objects.get_or_create(
                    series_instance_uid=series_uid,
                    defaults={
                        'study': study,
                        'modality': modality,
                        'description': series_desc,
                        'series_number': series_number
                    }
                )

                # Extract Image Data
                sop_uid = str(ds.get('SOPInstanceUID'))
                instance_number = ds.get('InstanceNumber')
                if instance_number:
                    instance_number = int(instance_number)
                
                # Metadata (convert dataset to JSON serializable dict)
                # We only take a subset or convert carefully
                metadata = {}
                for elem in ds:
                    if elem.keyword and elem.keyword != 'PixelData':
                        try:
                            val = elem.value
                            if isinstance(val, (int, float, str)):
                                metadata[elem.keyword] = val
                            elif isinstance(val, pydicom.multival.MultiValue):
                                metadata[elem.keyword] = list(val)
                        except:
                            pass

                ImageInstance.objects.get_or_create(
                    sop_instance_uid=sop_uid,
                    defaults={
                        'series': series,
                        'file_path': file_path,
                        'instance_number': instance_number,
                        'metadata': metadata
                    }
                )
                count += 1

            except pydicom.errors.InvalidDicomError:
                # Not a DICOM file, skip
                continue
            except Exception as e:
                errors.append(f"Error processing {file_path}: {str(e)}")
    
    return count, errors
