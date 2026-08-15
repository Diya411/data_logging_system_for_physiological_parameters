import socket
import pandas as pd
import time

BROADCAST_IP = "255.255.255.255"
BROADCAST_IP2 = "192.168.1.255"
PORT = 5005
CSV_FILE = "patient_data1.csv"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

last_row = 0

print("Patient Simulator Active")

while True:

    try:

        df = pd.read_csv(CSV_FILE)

        if last_row >= len(df):
            time.sleep(1)
            continue

        row = df.iloc[last_row]
        last_row += 1

        required_cols = ["HR", "SpO2", "RR", "Temp", "BP"]

        if row[required_cols].isnull().any():
            print("Skipping row with NaN values")
            continue

        hr = int(row["HR"])
        spo2 = int(row["SpO2"])
        rr = int(row["RR"])
        temp = float(row["Temp"])
        sys, dia = map(int,row["BP"].split("/"))

        alerts = []

        if hr < 60 or hr > 100:
            alerts.append("Heart Rate Abnormal")

        if spo2 < 95:
            alerts.append("Low SpO2")

        if rr < 12 or rr > 20:
            alerts.append("Respiration Abnormal")

        if temp < 36 or temp > 38:
            alerts.append("Temperature Abnormal")

        if sys < 90 or sys > 140 or dia < 60 or dia > 90:
            alerts.append("Blood Pressure Abnormal")

        if alerts:

            msg = f"BED04 | HR:{hr} | SpO2:{spo2} | RR:{rr} | Temp:{temp} | BP:{sys}/{dia}\n" + "; ".join(alerts)

            # sock.sendto(msg.encode(), (BROADCAST_IP, PORT))
            # sock.sendto(msg.encode(), (BROADCAST_IP2, PORT))
            # print("Broadcasted:",msg)

        time.sleep(2)

    except Exception as e:
        print(e)


