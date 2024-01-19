import os
import csv
import time

from pyModeS.decoder import adsb

print("===== Decode ADS-B sample data=====")

script_dir = os.path.dirname(__file__)
rel_path = os.path.normcase("data/sample_data_adsb.csv")
abs_file_path = os.path.join(script_dir, rel_path)

msg0 = None
msg1 = None

tstart = time.time()
with open(abs_file_path, "r") as infile:
    for i, r in enumerate(csv.reader(infile)):
        ts = int(r[0])
        m = r[1].encode()

        icao = adsb.icao(m)
        tc = adsb.typecode(m)

        if 1 <= tc <= 4:
            print(i, ts, m, icao, tc, adsb.category(m), adsb.callsign(m))
        if tc == 19:
            print(i, ts, m, icao, tc, adsb.velocity(m))
        if 5 <= tc <= 18:
            if adsb.oe_flag(m):
                msg1 = m
                t1 = ts
            else:
                msg0 = m
                t0 = ts

            if msg0 and msg1:
                pos = adsb.position(msg0, msg1, t0, t1)
                alt = adsb.altitude(m)
                print(i, ts, m, icao, tc, pos, alt)


dt = time.time() - tstart

print("Execution time: {} seconds".format(dt))
