#!/usr/bin/env python3
"""
Assignment to Endpoint Validation Script

This script checks for the presence of two specific NPIs in three specific CSV files using system grep calls.
It is NOT general-purpose and does NOT perform any database operations.

NPIs to check:
- 1043699168 (Woodridge Primary Clinic)
- 1023008976 (Dr Hussain)

Files to check:
- PECOS Enrollment: /Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Enrollment_Extract_2025.04.01.csv
- PECOS Reassignment: /Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Reassignment_Extract_2025.04.01.csv
- FHIR Endpoint: /Users/ftrotter/gitgov/ftrotter/ehr_fhir_npi_slurp/data/output_data/clean_npi_to_org_fhir_url.csv

The file structure of the enrollment file is:
NPI,PECOS_ASCT_CNTL_ID,ENRLMT_ID,PROVIDER_TYPE_CD,PROVIDER_TYPE_DESC,STATE_CD,FIRST_NAME,MDL_NAME,LAST_NAME,ORG_NAME

Process:
1. Grep for the two NPIs in the enrollment file and extract their ENRLMT_IDs.
2. Use those ENRLMT_IDs to grep the reassignment file.
3. Grep for Woodridge's NPI in the FHIR endpoint file.
4. Report if the expected matches are found.

Expected:
- Two rows for the two NPIs in the enrollment file
- One row in the reassignment file showing Dr. Hussain assigns payment to Woodridge, using ENRLMT_IDs
- One row in the EHR file matching the NPI of Woodridge

This script prints the matching lines and reports whether the expectations are met.
"""

import subprocess
import csv

NPIS = {
    "1043699168": "Woodridge Primary Clinic",
    "1023008976": "Dr Hussain"
}

FILES = {
    "PECOS Enrollment": "/Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Enrollment_Extract_2025.04.01.csv",
    "PECOS Reassignment": "/Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Reassignment_Extract_2025.04.01.csv",
    "FHIR Endpoint": "/Users/ftrotter/gitgov/ftrotter/ehr_fhir_npi_slurp/data/output_data/clean_npi_to_org_fhir_url.csv"
}

def grep_npi_in_file(npi, file_path):
    try:
        result = subprocess.run(
            ["grep", "-w", npi, file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().splitlines()
        else:
            return []
    except Exception as e:
        return [f"Error searching for {npi} in {file_path}: {e}"]

def grep_enrlmt_id_in_file(enrlmt_id, file_path):
    try:
        result = subprocess.run(
            ["grep", "-w", enrlmt_id, file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().splitlines()
        else:
            return []
    except Exception as e:
        return [f"Error searching for ENRLMT_ID {enrlmt_id} in {file_path}: {e}"]

def extract_enrlmt_id_from_enrollment_line(line):
    # Enrollment file columns:
    # NPI,PECOS_ASCT_CNTL_ID,ENRLMT_ID,PROVIDER_TYPE_CD,PROVIDER_TYPE_DESC,STATE_CD,FIRST_NAME,MDL_NAME,LAST_NAME,ORG_NAME
    try:
        reader = csv.reader([line])
        row = next(reader)
        if len(row) >= 3:
            return row[2]
        else:
            return None
    except Exception:
        return None

def main():
    summary = {
        "enrollment": {"1043699168": 0, "1023008976": 0, "1043699168_enrlmt_id": None, "1023008976_enrlmt_id": None},
        "reassignment": {"woodridge_enrlmt_id": 0, "hussain_enrlmt_id": 0, "assignment_match": False},
        "fhir": {"1043699168": 0}
    }

    # Step 1: Grep for NPIs in enrollment file and extract ENRLMT_IDs
    print(f"\n=== Checking file: PECOS Enrollment ===")
    enrollment_path = FILES["PECOS Enrollment"]
    npi_to_enrlmt_id = {}
    for npi in NPIS:
        lines = grep_npi_in_file(npi, enrollment_path)
        summary["enrollment"][npi] = len(lines)
        print(f"\n-- Results for NPI {npi} ({NPIS[npi]}) --")
        if lines:
            for line in lines:
                print(line)
                enrlmt_id = extract_enrlmt_id_from_enrollment_line(line)
                if enrlmt_id:
                    npi_to_enrlmt_id[npi] = enrlmt_id
                    summary["enrollment"][f"{npi}_enrlmt_id"] = enrlmt_id
        else:
            print(f"No matches found for NPI {npi} in PECOS Enrollment.")

    # Step 2: Use ENRLMT_IDs to grep reassignment file
    print(f"\n=== Checking file: PECOS Reassignment ===")
    reassignment_path = FILES["PECOS Reassignment"]
    woodridge_enrlmt_id = npi_to_enrlmt_id.get("1043699168")
    hussain_enrlmt_id = npi_to_enrlmt_id.get("1023008976")
    reassignment_lines = {}
    if woodridge_enrlmt_id:
        lines = grep_enrlmt_id_in_file(woodridge_enrlmt_id, reassignment_path)
        summary["reassignment"]["woodridge_enrlmt_id"] = len(lines)
        reassignment_lines["woodridge"] = lines
        print(f"\n-- Results for Woodridge ENRLMT_ID {woodridge_enrlmt_id} --")
        if lines:
            for line in lines:
                print(line)
        else:
            print(f"No matches found for Woodridge ENRLMT_ID {woodridge_enrlmt_id} in PECOS Reassignment.")
    else:
        print("Could not determine Woodridge ENRLMT_ID from enrollment file.")

    if hussain_enrlmt_id:
        lines = grep_enrlmt_id_in_file(hussain_enrlmt_id, reassignment_path)
        summary["reassignment"]["hussain_enrlmt_id"] = len(lines)
        reassignment_lines["hussain"] = lines
        print(f"\n-- Results for Dr Hussain ENRLMT_ID {hussain_enrlmt_id} --")
        if lines:
            for line in lines:
                print(line)
        else:
            print(f"No matches found for Dr Hussain ENRLMT_ID {hussain_enrlmt_id} in PECOS Reassignment.")
    else:
        print("Could not determine Dr Hussain ENRLMT_ID from enrollment file.")

    # Check for assignment row: a line in reassignment file containing both ENRLMT_IDs
    found_assignment = False
    if woodridge_enrlmt_id and hussain_enrlmt_id:
        try:
            result = subprocess.run(
                ["grep", "-w", hussain_enrlmt_id, reassignment_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.strip().splitlines():
                    if woodridge_enrlmt_id in line:
                        found_assignment = True
                        print("\n-- Found assignment row (Dr Hussain assigns payment to Woodridge via ENRLMT_IDs):")
                        print(line)
            summary["reassignment"]["assignment_match"] = found_assignment
            if not found_assignment:
                print("\n-- No row found where Dr Hussain assigns payment to Woodridge in reassignment file (via ENRLMT_IDs).")
        except Exception as e:
            print(f"Error searching for assignment row: {e}")

    # Step 3: Grep for Woodridge NPI in FHIR Endpoint
    print(f"\n=== Checking file: FHIR Endpoint ===")
    fhir_path = FILES["FHIR Endpoint"]
    lines = grep_npi_in_file("1043699168", fhir_path)
    summary["fhir"]["1043699168"] = len(lines)
    print(f"\n-- Results for NPI 1043699168 (Woodridge Primary Clinic) --")
    if lines:
        for line in lines:
            print(line)
    else:
        print("No matches found for NPI 1043699168 in FHIR Endpoint.")

    # Print summary
    print("\n====================")
    print("Validation Summary:")
    print("====================")
    # Enrollment
    if summary["enrollment"]["1043699168"] >= 1 and summary["enrollment"]["1023008976"] >= 1:
        print("✔ Enrollment file: Found at least one row for each NPI (Woodridge and Dr Hussain).")
    else:
        print("✘ Enrollment file: Missing row(s) for one or both NPIs.")
    # Reassignment
    if summary["reassignment"]["assignment_match"]:
        print("✔ Reassignment file: Found row where Dr Hussain assigns payment to Woodridge (via ENRLMT_IDs).")
    else:
        print("✘ Reassignment file: Did NOT find row where Dr Hussain assigns payment to Woodridge (via ENRLMT_IDs).")
    # FHIR
    if summary["fhir"]["1043699168"] >= 1:
        print("✔ FHIR Endpoint file: Found at least one row for Woodridge NPI.")
    else:
        print("✘ FHIR Endpoint file: No row found for Woodridge NPI.")

if __name__ == "__main__":
    main()
