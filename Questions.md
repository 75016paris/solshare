**Inverter plants** :
Where is DGL (GGI) no adress ??? no plant_type ???
        Gazzipur
Could we have exact adress ?? (to be able to define exact location/orientation)

Plant_capacity : is this kilowatt peak ?
(killowat peak)
min 4.25 (SOLshatre LM Tower)
max 1280.40 (DGL GGI)

System_type : no value is Off Grid

Status : ???
Inative mean > no data


**generator_data_logs** (54322 x 6):
only for :
NAL (GGI) = 2025-03-12 > 2025-10-23
ACML (GGI) - 2025-03-10 > 2025-10-23
CAL (GGI) - 2025-09-11 > 2025-10-23

What is Device ?
- DM1, 2, 3 > data collector
- MX 01, 02, 03 > data collector

What is state ?
off 45575 (83%)
on 8747 (16%)

What is power (only 8747/54322 values) ?
0 (7%)
Some value are negative, why ?
NAL (GGI) min -131072
CAL (GGI) min -74.266
ACML (GGI) min 0

NAL (GGI) max 474458.084
CAL (GGI) max 326987.701
ACML (GGI) max 448183.670

3 plants :
mean 141272
median 100597.40

Plants (Value only for 3 plants):
NAL (GGI)                      26315
ACML (GGI)                     15931
CAL (GGI)                      12076

DGL (GGI)                          ?
SOLshare LM Tower                  ?
BHC                                ?
ACCL (GGI)                         ?
HKL (GGI)                          ?
Unilever Sales Depot Bogura        ?
KCL (SOLshare)                     ?
Faruk Auto Garage Rajshahi         ?



**Inverter Daily Generation** (6022 x 4):
date 2022-02-11 > 2025-10-22

inconsistent date ?

NOT IN PROJECTS (Projects dashboard page) :
KCL (SOLshare) (2022-11-12) 1407
Faruk Auto Garage Rajshahi (2022-02-11) 583
SOLshare LM Tower (2023-02-09) 550
Unilever Sales Depot Bogura (2022-10-14) 328
BHC (2022-11-15) 22

IN PROJECTS (Projects dashboard page) :
CAL (GGI) (2023-11-27) 656
HKL (GGI) (2023-12-17) 645
NAL (GGI) (2023-11-21) 633
ACML (GGI) (2024-02-13) 598
ACCL (GGI) (2023-12-03) 509
DGL (GGI) (2025-07-01) 91


What is generation amount ? (value in parenthesis are python-object with ",")
max 17237.85 - (999.9)
min -15677.81 - (-1,140.7) ???
mean 572.89






**Inverter weather logs** (4148 x 7):
What is this, where the data come from ?
Plant ID doesnt match any location, plant_id in inverter_plants ?
2023-02-28 > 2023-10-01

Temperature ?
module temperature ?
ambient temperature ?
Solar irradiation ?






**plants billing meter logs** :
2024-09-10 > 2025-10-22 (beware different date from plants meter data logs hourly)
Only live Plant


NAL (GGI)     1209 (3 meters)
ACML (GGI)     873 (3 meters)
ACCL (GGI)     796 (2 meters)
HKL (GGI)      444 (2 meters)
DGL (GGI)      428 (4 meters)
CAL (GGI)      398 (1 meter)

**METER_ID > PLANT**
12019165 = ACML (GGI)
12667024 = ACML (GGI)
14894877 = ACML (GGI) (meter_reading always 0)

11811476 = NAL (GGI)x
11811369 = NAL (GGI)x
12635561 = NAL (GGI)x

15834240 = ACCL (GGI)x
15834239 = ACCL (GGI)x

11848078 = CAL (GGI)x

11838324 = HKL (GGI)x
16008274 = HKL (GGI)x

15959518 = DGL (GGI)x
15848112 = DGL (GGI)x
15959516 = DGL (GGI)x
15848111 = DGL (GGI)x




**plants meter data logs hourly** :
2025-04-17 > 2025-10-23 (beware different date from plants billing meter logs)
Only live Plant

What are the meter_id ??
What is guid ??

What is the unit of meter_reading ??
min 35059847.0
max 590845062.0

**METER_ID > PLANT**
12019165 = ACML (GGI)x
12667024 = ACML (GGI)x
14894877 = ACML (GGI) (NOT PRESENT in hourly)

11811476 = NAL (GGI)x
11811369 = NAL (GGI)x
12635561 = NAL (GGI)x

15834240 = ACCL (GGI)x
15834239 = ACCL (GGI)x

11848078 = CAL (GGI)x

11838324 = HKL (GGI) (NOT PRESENT in hourly)
16008274 = HKL (GGI)x

15959518 = DGL (GGI)x
15848112 = DGL (GGI)x
15959516 = DGL (GGI)x
15848111 = DGL (GGI)x
