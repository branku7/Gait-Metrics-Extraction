import re
import csv
import json


def getFileInfo(directory):
    with open(directory, mode="r") as csvfile:
        arrayFiles = {}
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            newFilename = row["filename"].split(".cwa")[0]
            arrayFiles[newFilename] = row
        return arrayFiles


def getReportStepsFromCsv(
    filename,
    location_jsons="./reports/data/",
    dir_fileinfo="./reports/file-map/inputFileInfo.csv",
):
    """
    This function will get the corresponding steps for the exercise
    indetified at the end of the filename i.e. "_walk"

    Important for the data to be organized in the same way.
    """
    # Get exercise name
    aux = filename.split("_")
    exercise_name = aux[-1].split(".")[0]
    exercise_name = exercise_name.lower()

    # Get file name without the name of exercise at the end
    allFileSeg = aux[0] + "".join("_" + str(e) for e in aux[1:-1])

    # Get Report Code and Original Name
    report_code, original_data_filename, _ = get_FileCode_and_Name(
        allFileSeg, FileInfo_dir=dir_fileinfo
    )

    # Get Json Data and AndroidKey
    json_data = get_JsonData(report_code, location=location_jsons)
    curr_android_key = get_AndroidKey(json_data, original_data_filename)

    # Get Exercise Information
    exercise_report = (
        json_data.get("AndroidReport").get(curr_android_key).get(exercise_name)
    )

    # S2S
    if exercise_name == "s2s":
        print("To be Developed")  # TODO No steps here though
        return [0, 0, 0]

    # Walk
    if exercise_name == "walk":

        result = list()
        first_steps = 0
        if exercise_report.get("first_steps") != None:
            first_steps = exercise_report.get("first_steps")
        else:
            first_steps = exercise_report.get("npw_first").get("first_steps")

        result.append(first_steps)

        second_steps = 0
        if exercise_report.get("second_steps") != None:
            second_steps = exercise_report.get("second_steps")
        else:
            second_steps = exercise_report.get("npw_second").get("second_steps")

        result.append(second_steps)

        third_steps = 0
        if exercise_report.get("third_steps") != None:
            third_steps = exercise_report.get("third_steps")
        else:
            third_steps = exercise_report.get("npw_third").get("third_steps")

        result.append(third_steps)

    # Tug
    if exercise_name == "tug":
        print("To be Developed")  # TODO Some steps, but is it worth it?
        return [0, 0, 0]

    return result


def get_AndroidKey(json_data, original_data_filename):
    lab_report_keys = json_data.get("LabReport")

    curr_android_key = ""

    # Get Android Key
    for key in list(lab_report_keys):
        curr_filename = lab_report_keys.get(key).get("filename")
        if curr_filename == original_data_filename:
            curr_android_key = lab_report_keys.get(key).get("androidKey")
            break
    return curr_android_key


def get_JsonData(report_code, location="./reports/data/"):
    json_fid = open(
        location + report_code + ".json", "r", encoding="utf-8"
    ) 
    json_data = json.load(json_fid)

    return json_data


def get_FileCode_and_Name(
    filename, FileInfo_dir="./reports/file-map/inputFileInfo.csv"
):
    # Get file with all the corresponding codes
    mapFileInfo = getFileInfo(FileInfo_dir)

    fileInfo = mapFileInfo[filename]
    original_data_filename = fileInfo["newFilename"]
    report_code = fileInfo["code"]
    patient_name = fileInfo["name"]

    return report_code, original_data_filename, patient_name


def getPatientInfo(
    filename,
    location_jsons="./reports/data/",
    dir_fileinfo="./reports/file-map/inputFileInfo.csv",
    ): 
    """
    This function will get the corresponding steps for the exercise
    indetified at the end of the filename i.e. "_walk"

    Important for the data to be organized in the same way.
    """
    # Get exercise name
    aux = filename.split("_")
    exercise_name = aux[-1].split(".")[0]
    exercise_name = exercise_name.lower()

    # Get file name without the name of exercise at the end
    allFileSeg = aux[0] + "".join("_" + str(e) for e in aux[1:-1])

    # Get Report Code and Original Name
    report_code, original_data_filename, patient_name = get_FileCode_and_Name(
        allFileSeg, FileInfo_dir=dir_fileinfo
    )

    # Get Json Data and AndroidKey
    json_data = get_JsonData(report_code, location=location_jsons)
    curr_android_key = get_AndroidKey(json_data, original_data_filename)

    meta_data = json_data.get('AndroidReport').get(curr_android_key).get('metadata')
        
    patient_age = meta_data.get('age')
    if(patient_age == 0 or patient_age == None ):
        patient_age = json_data.get('age')
    
    patient_height = meta_data.get('height')
    if(patient_height == 0 or patient_height == None):
        patient_height = json_data.get('height')
    
    patient_weight = meta_data.get('weight')
    if(patient_weight == 0 or patient_weight == None):
        patient_weight = json_data.get('weight')
    
    patient_info = dict()
    patient_info['name'] = patient_name
    patient_info['age'] = patient_age
    patient_info['height'] = patient_height
    patient_info['weight'] = patient_weight
    patient_info['code'] = report_code
    
    return patient_info
