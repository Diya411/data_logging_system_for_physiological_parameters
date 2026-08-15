import csv
import time
import os

HL7_FILE = "patient_data.hl7"
CSV_FILE = "patient_data.csv"

last_position = 0

print("HL7 Converter Running")

while True:

    rows=[]
    patient_id=""
    timestamp=""
    vitals={}

    def append_current():
        if vitals:
            rows.append([
                timestamp,
                patient_id,
                vitals.get("HR"),
                vitals.get("BP"),
                vitals.get("SPO2"),
                vitals.get("TEMP"),
                vitals.get("RR")
            ])

    with open(HL7_FILE,"r") as f:

        f.seek(last_position)

        for line in f:

            fields=line.strip().split("|")

            if not fields:
                continue

            if fields[0]=="PID":
                append_current()
                patient_id=fields[3]
                vitals={}

            elif fields[0]=="OBR":
                timestamp=fields[7]

            elif fields[0]=="OBX":
                param=fields[3].split("^")[0]
                vitals[param]=fields[5]

        append_current()

        last_position=f.tell()

    if rows:

        file_exists = os.path.isfile(CSV_FILE)

        with open(CSV_FILE, "a", newline="") as csvfile:

            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(["Timestamp","PatientID","HR","BP","SpO2","Temp","RR"])

            writer.writerows(rows)

    time.sleep(2)
