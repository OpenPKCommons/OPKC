# Main Literature List
Comprehensive, authoritative list of papers scanned for possible inclusion in open pathogen kinetics commons.

## Key
- DE ✅ = data exists
	- DE-NEA ✳️ = not easily accessible
	- as in is clearly there at individual scale but would need to be extracted or requested
- DME ❇️ = data may exist, worth following up more in-depth
	- as in would definitely need to request, and figures do not display individual resolution
	- this is more work than DE-NEA
	- * an asterisk denotes that this data seems especially difficult to track down
- NA ❎ = not applicable, not something we can use for whatever reason
- MO 🤖 = modeling only
- DAI = data already included
	- e.g. data from these references have already been included or superseded by another DE reference
	- these are listed in main_list_list to prevent redundant scanning
- pathogen(s)
	- [`SARS2`, `Flu`, `FMD`, `WestNile`, `SARS`, `MERS`, `Smallpox`, `HIV`, `Bact Res` #baterial resistance, `Dengue`]
- tags
	- pathogen strain or subtype (e.g. `H5N1`, `Omicron`)
	- species studied, if other than human
		- [`mosq`, `cows`, `sheep`, `birds`, `in vitro`]
	1. XS 🌐 = cross-sectional data (may be of use for model parameters, but isn't individual-level empirical data itself)
	2. sx 🤧 = symptom trajectory information
	3. MA ♻️ = meta-analysis or review that combines other original data sources
	4. REF = paper has references that should be scanned for data availability
	5. LAB, LOD, SEQ, Ab = paper has lab data that may be useful (e.g. culture, LOD, genetic sequencing, antibodies)
	6. BIN = infection status is binary, positive/negative
	7. MOSP = mobility or spatial data
	8. PACK = package
	9. VAX = vaccination data

# Literature List
## Datasets already ingested in our schema
### Digested => MVP v1 data has been ingested and added to schema
### Additional data may be available from source for schema v2 (e.g. symptom or vaccination data)
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | By | Additional data? |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| 10.1038/s41564-022-01105-z | Ke2022daily | `DIGESTED` | `SARS2` | | Stephen | No |
| 10.1038/s41467-023-41941-z | Kissler2023 | `DIGESTED` | `SARS2` | | Stephen | Yes |
| 10.1371/journal.pbio.3002463 | Russell2024 | `DIGESTED` | `SARS2` | | Stephen | Yes |
| 10.1126/sciimmunol.adj9285 | Wagstaffe2024 | `DIGESTED` | `SARS2` | | Carrie | Yes - revisit source|
| 10.1016/S1473-3099(24)00183-X | Wongnak2024 | `DIGESTED` | `SARS2` | | Stephen | Yes |
| 10.1016/S2213-2600(22)00226-0 | Hakki2022 | `DIGESTED` | `SARS2` | `VAX` `LAB`| Oliver | Yes |
| 10.1128/jcm.01785-21 | Savela2022 | `DIGESTED` | `SARS2` | `sx` | Oliver | Yes |
| 10.1126/scitranslmed.abo5019 | Waickman2022 | `DIGESTED` | `Dengue` | `sx` `LAB` | Oliver | Yes |
| 10.1038/s41564-024-01668-z | Waickman2024 | `DIGESTED` | `Dengue` | `LAB` | Oliver | Yes |
| 10.1038/s41591-022-01816-0 | Puhach2022 | `DIGESTED` | `SARS2` `VAX` | | Carrie | Yes |
| 10.1126/science.abi5273 | Jones2021 | `DIGESTED` | `SARS2` | `LAB` | Carrie | Yes |
| 10.1038/s41586-024-07849-4 | Eales_Caserta | `DIGESTED` | | Ellen | Yes |
| 10.1038/s41586-024-08166-6 | Eales_Baker | `DIGESTED` | | Ellen | Yes|
| 10.1038/s41586-024-08063-y | Eales_Halwe | `DIGESTED` | | Ellen | No |
| 10.7554/eLife.92606.3 | Vuong2024 | `DIGESTED` | `Dengue` | `LAB` | Oliver | Yes |
| 10.1038/s41467-020-20568-4 | vanKampen2021 | `DE` | `SARS2` | `LAB` | Carrie | No |
| 10.1101/2025.07.02.662782 | Alahakoon2025TrackingWestNile | `DIGESTED` | `WestNile` | `mosq` `birds` `MOSP` | Carrie | Yes |
| 10.7326/M20-1495 | Kucirka2020 | `Separating out` | `SARS2` | `MA` | Carrie | Yes |
| 10.1038/s41467-025-61553-z | Peña-Mosca2025  | `DIGESTED` | `Flu` |`H5N1` `cows` `sx` `LAB`| Oliver | Yes |
| 10.1038/s41564-025-01998-6 | Facciuolo et al 2025 | `DIGESTED` | `Flu` |`H5N1` `cows` `sx` `LAB` `Ab` | Ellen | Yes |

Count = 20

## DE = DATA EXISTS (in priority order)
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | INGEST-IN-PROGRESS-BY? | Data link |
|:---|:---|:---:|:---:|:---:|:---|:---|
| 10.1371/journal.ppat.1012171 | Snedden et al 2024 | `DE` | `SARS2` | `macaque` | | [Zenodo](https://zenodo.org/records/10947025) |
| 10.1093/cid/ciaa344 | Zhao 2020 | `DE` | `SARS2` | | Carrie - from Kucirka 2020 | Data available in article and supplementary materials (PMC Open Access) |
| 10.1101/2020.03.06.20031856 | Liu 2020 | `DE` | `SARS2` | | Carrie - from Kucirka 2020 | Data included within the preprint article |
| 10.1093/cid/ciaa310 | Guo 2020 | `DE` | `SARS2` | | Carrie - from Kucirka 2020 | Data available in article and supplementary materials (PMC Open Access) |
| 10.1038/s41586-020-2196-x | Wölfel 2020 | `DE` | `SARS2` | | Carrie - from Kucirka 2020 | Viral load, sequencing, and isolation data included in article; no separate repository listed |
| 10.1093/cid/ciaa424 | Danis 2020 | `DE` | `SARS2` | | Carrie - from Kucirka 2020 | Outbreak investigation data available in article and supplementary materials |
| 10.1101/2020.03.09.20032896 | Kujawski 2020 | `DE` | `SARS2` | | Carrie - from Kucirka 2020 | Data stated as “available upon request” |
| 10.1001/jama.2020.3786 | Wang 2020 | `DE` | `SARS2` | | Carrie - from Kucirka 2020 | Specimen testing data included in the article |
| 10.1093/infdis/jiaf138 | Li et al 2025 | `DE` | `RSV` | | UNCLAIMED | [github](https://github.com/keli5734/RSV_Viral_Dynamics_Study/tree/main) |
Count = 9

## DE-NEA = Data exists, not easily accesible (alphabetized)
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | AUTHOR_CONTACTED? |
|:---|:---|:---:|:---:|:---:|---:|
| 10.1007/s40121-025-01235-x | Berger et al 2025 | `DE-NEA` | `SARS2` |  | No |
| Preprint | Blanquart et al 2021 | `DE-NEA` | `SARS2` |  | No |
| 10.1056/nejmc2202092 | Boucau et al 2022 | `DE-NEA` | `SARS2` | `Omicron` `sx` | On deck |
| 10.1093/aje/kwm375 | Carrat et al 2008 | `DE-NEA` | `Flu` | `H1N1` `sx` | On deck |
| 10.1016/s2666-5247(20)30172-5 | Cevik et al 2020 | `DE-NEA` | `SARS2` `SARS` `MERS` | `MA` `REF` | No |
| 10.7326/0003-4819-151-7-200910060-00142 | Cowling et al 2009 | `DE-NEA` | `Flu` | `H1N1` | On deck |
| 10.1098/rsif.2016.0289 | Hadjichrysanthou et al 2016 | `DE-NEA` | `Flu` | `H1N1` | On deck |
| 10.1038/s41591-020-0869-5 | He et al 2020 | `DE-NEA` | `SARS2` |  | No |
| 10.1038/s41591-022-01780-9 | Killingley et al 2022 | `DE-NEA` | `SARS2` | `sx` `LAB` | On deck |
| 10.1016/j.antiviral.2004.04.005 | Lee et al 2004 | `DE-NEA` | `RSV` | `sx` | No |
| 10.1093/biostatistics/kxaa009 | Mahsin et al 2019 | `DE-NEA` | `Flu` | `H1N1` `MOSP` | No |
| 10.1038/s44298-025-00132-x | Mehta et al 2025 | `DE-NEA` | `SARS` `Flu` `RSV` | `H3N2` | No |
| 10.1128/iai.29.2.348-355.1980 | Murphy et al 1980 | `DE-NEA` | `Flu` | `H1N1` | No |
| 10.1101/700401 | Prague et al 2019 | `DE-NEA` | `HIV` `SIV` | `LAB` `VAX` `Ab` | No |
| 10.1016/j.antiviral.2020.104763 | Sloan et al 2020 | `DE-NEA` | `Flu` | `XS` `H1N1` | On deck |
| 10.1001/jamanetworkopen.2021.42796 | Stankiewicz et al 2022 | `DE-NEA` | `SARS2` |  | No |
| 10.1038/s41586-020-2196-x | Wolfel et al 2020 | `DE-NEA` | `SARS2` |  | No |
| 10.3389/fmicb.2019.02342  | Yuko Sakai-Tagawa et al 2019 | `DE-NEA` | `Flu` | `H1N1` `H3N2` `H5N1` `H5N6` `H7N9` `Victoria` `Yamagata` | No |

Count = 18

## DME = Data MAY exist
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | By |
|:---|:---|:---:|:---:|:---:|---:|
| 10.1111/jgs.19499 | Katz et al 2025 | `DME` | | | Ellen |
| 10.1038/s41467-025-61737-7 | Chong et al 2025 | `DME` | | | Ellen |
| 10.1056/NEJMoa2116154 | Shmoele-Thoma 2022 Vaccine | `DME` | | | Ellen via Casey |
| 10.1093/cid/civ909 | Ip 2016 Dynamic | `DME` | | `XS` `sx` | Ellen via Casey |
| 10.1002/psp4.13022 | Zhang et al 2023 | `DME` | | | Ellen |
| 10.1093/ofid/ofac192 | Ke et al 2022 Longitudinal | `DME` | | | Ellen |
| 10.21203/rs.3.rs-6900680/v1 | Lee et al 2025 | `DME` | | | Ellen |
| 10.1038/s41586-024-07575-x | Lindeboom et al 2024 | `DME` | | | Ellen |
| 10.1086/652241 | Lau et al 2010 | `DME` | | `sx` | Ellen via Casey |
| 10.1172/JCI1355 | Hayden et al 1998 | `DME` | | | Ellen via Casey |
| 10.3851/IMP2629 | Bagga et al 2013 | `DME` | | `sx` | Ellen via Casey |
| doi:10.1017/S0950268813001672 | Noh et al 2013 | `DME` | | `sx` | Ellen via Casey |
| 10.1111/j.1469-0691.2010.03399.x | Giannella et al 2010 | `DME` | | | Ellen via Casey |
| 10.1093/cid/ciaa638 | Bullad et al 2020 | `DME` | | `XS` `LAB` | Ellen RR |
| 10.1093/cid/ciq026 | Bhattarai et al 2011 | `DME` | | `sx` `LAB` | Ellen RR |
| 10.1086/656582 | Papenburg et al 2010 | `DME` | | `sx` `BIN` | Ellen RR |
| 10.1093/infdis/jis450 | Loeb et al 2012 | `DME` | | `sx` | Ellen RR |
| 10.1093/aje/kwq071 | Suess et al 2010 | `DME` | | `sx` | Ellen RR |
| 10.1371/journal.pone.0051653 | Suess et al 2012 | `DME` | | `sx` | Ellen RR |
| 10.1001/jamainternmed.2022.1827 | Chu et al 2022 | `DME` | | `sx` | Ellen RR |
| 10.1007/978-1-4684-5239-6_7 | Kilbourne et al 1987 | `DME` | | `REF` `sx` | Ellen RR |
| 10.1177/003335490912400205 | Patrozou et al 2009 | `DME` | | `MA` `REF` | Ellen RR |
| 10.1111/irv.12216 | Fielding et al 2014 | `DME` | | `MA` `REF` | Ellen RR |
| 10.1093/cid/ciq028 | Donnelly et al 2011 | `DME` | | `MA` `REF` | Ellen RR |
| 10.7326/0003-4819-151-7-200910060-00142 | Cowling et al 2009 | `DME` | | | Ellen RR |
| 10.1093/cid/ciaa1706 | Pekosz et al 2021 | `DME` | | | Ellen RR |
| 10.1016/j.cmi.2022.07.010 | Kirby et al 2022 | `DME` | | | Ellen RR |
| 10.1002/jmv.21664 | Wang et al 2010 | `DME` | | | Ellen RR |
| 10.3181/00379727-122-31255 | Alford et al 1966 | `DME` | | | Ellen RR |
| 10.1086/650458 | Ng et al 2010 | `DME` | | | Ellen RR |
| 10.1093/infdis/jiab337 | Smith et al 2021 | `DME` | | | Ellen RR |
| 10.1093/cid/ciac510 | Bouton et al 2022 | `DME` | | | Ellen RR |
| 10.1001/jama.1996.03530280047035 | Hayden et al 1996 | `DME` | | | Ellen RR |
| 10.1016/s0140-6736(09)62126-7 | Miller et al 2010 | `DME` | | | Ellen RR |
| 10.1086/314938 | Fritz et al 1999 | `DME` | | | Ellen RR |
| 10.1126/science.1086478 | Riley et al 2003 | `DME` | `SARS` | | Ellen |
| 10.1126/science.1086616 | Lipsitch et al 2003 | `DME` | `SARS` | | Ellen |
| 10.1016/S0140-6736(03)13410-1 | Donnelly et al 2003 | `DME` | `SARS` | * | Ellen |
| 10.1016/S0140-6736(03)13412-5 | Peiris et al 2003 | `DME` | `SARS` | `sx` `LAB` | Ellen |
| 10.1128/CVI.00229-08 | Gagneur et al 2008 | `DME` | `Measles` | `LAB` `Ab` | Ellen GH |
| 10.1515/ijb-2013-0026 | Deeth et al 2013 | `DME` |  | * | 
| 10.1126/science.1065973 | Keeling et al 2001 | `DME` | `FMD` | * | 
| 10.1186/1746-6148-2-3 | Savill et al 2006 | `DME` | `FMD` | * | 
| 10.1056/NEJMoa2116154 | Shmoele-Thoma et al 2022 | `DME` | `RSV` |  | 
| 10.1371/journal.pone.0051653 | Suess et al 2012 | `DME` |  | `sx` | 

Count = 45

## IDed paper in scanning queue
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | By |
|:---|:---|:---:|:---:|:---:|---:|
| 10.1016/S2666-5247(23)00005-8 | Galmiche et al 2023 | `IDed` | | | Ellen |
| 10.1016/S2666-5247(23)00101-5 | Zhou et al 2023 | `IDed` | | | Ellen |
| 10.3389/fimmu.2018.00323 | Ascough et al 2018 | `IDed` | | | Ellen |
| 10.1007/82_2022_257 | Dayananda et al 2022 | `IDed` | | | Ellen |
| 10.1097/QAD.0000000000000953 | Li et al 2016 | `IDed` | `HIV` | | Ellen |
| 10.1101/2025.10.24.25338576 | Bruce et al 2025 | `IDed` | `Flu` | | Dan Epidemics |
| 10.1371/journal.ppat.1012131 | VanInsberghe et al 2024 | `IDed` | `Flu` | `H1N1` `H3N2` | Dan Epidemics |
Count = 7+
*Consult verbose_main_lit_list.xlsx for full queue*

## MO = Modeling Only papers
| DOI | PaperNameString | Status/Classification | Tags | By |
|:---|:---|:---:|:---:|---:|
| 10.1016/j.epidem.2025.100843 | Xu et al 2025 | `MO` | | Ellen |
| 10.1126/sciadv.abd5393 | Larremore et al 2020 | `MO` | | Ellen via Casey |
| 10.1002/wsbm.129 | Smith 2010 | `MO` | `REF` | Ellen via Casey |
| 10.1128/jvi.01623-05 | Baccam et al 2006 | `MO` | `DAI` | Ellen |
| 10.1038/nature04153 | Lloyd et al 2005 | `MO` | `XS` `REF` | Ellen RR |
| 10.1128/jvi.01623-05 | Baccam et al 2006 | `MO` | `REF` | Ellen RR |
| 10.1371/journal.pcbi.1002588 | Pawelek et al 2012 | `MO` | `REF` | Ellen RR |
| 10.1093/aje/kwh092 | Longini et al 2004 | `MO` | `REF` | Ellen RR |
| 10.1038/nature04795 | Ferguson et al 2006 | `MO` | | Ellen RR |
| 10.1056/nejmoa0905498 | Cauchemez et al 2009 | `MO` | | Ellen RR |
| 10.1001/jamanetworkopen.2021.10071 | Holmdahl et al 2021 | `MO` | | Ellen RR |
| 10.1073/pnas.0307506101 | Fraser et al 2004 | `DE` | `MA` `MO` | Ellen RR |
| 10.1016/0025-5564(85)90064-1 | Rvachev et al 1985 | `MO` | `Flu` `H1N1` | Ellen |
| 10.3390/v9080197 | Cao et al 2017 | `MO` | `REF` | Dan |
| 10.1016/j.idm.2024.10.008 | Akter et al 2024 | `MO` | `FMD` |  | 
| 10.18637/jss.v098.i10 | Almutiry et al 2020 | `MO` |  | PACK | 
|  | Deardon et al 2010 | `MO` | `FMD` |  | 
| 10.1073/pnas.2011802117 | Lau et al 2020 | `MO` | SARS2 | MOSP | 
| 10.1016/j.sste.2024.100664 | Rahul et al 2024 | `MO` |  |  | 
| 10.32614/rj-2020-020 | Vineetha Warriyar et al 2020 | `MO` |  |  | 
| 10.1016/j.sste.2022.100497 | Ward et al 2022 | `MO` |  |  | 

Count = 21

### NA = Not Applicable
| DOI | PaperNameString | Status/Classification | Tags | By |
|:---|:---|:---:|:---:|---:|
| 10.2217/fmb.13.9 | Prendergast et al 2013 | `NA` | `XS` `MA` | Ellen |
| 10.1016/j.jinf.2020.06.067 | Walsh et al 2020 | `NA` | `MA` `REF` | Ellen RR |
| 10.1128/jcm.02881-20 | Lee et al 2021 | `NA` | `MA` `LOD` `REF` | Ellen RR |
| 10.3390/jcm10020328 | Kohmer et al 2021 | `NA` | `LOD` `LAB` | Ellen RR |
| 10.1038/nature04017 | Ferguson et al 2005 | `NA` | | Ellen RR |
| 10.1056/nejmp2025631 | Mina et al 2020 | `NA` | | Ellen RR |
| 10.3201/eid1510.091013 | Han et al 2009 | `NA` | | Ellen RR |
| 10.1056/nejmcp2117115 | Drain et al 2022 | `NA` | | Ellen RR |
| 10.1371/journal.ppat.1003205 | Milton et al 2013 | `NA` | | Ellen RR |
| 10.3201/eid1211.060426 | Tellier et al 2006 | `NA` | | Ellen RR |
| 10.1016/s2666-5247(21)00143-9 | Pickering et al 2021 | `NA` | `LOD` | Ellen RR |
| 10.1016/S0140-6736(00)02061-4 | Babiker et al 2000 | `NA` | `HIV`  | Ellen |
| 10.1016/S1473-3099(24)00416-X | Pham et al 2024 | `NA` | `Bact Res`  | Ellen GH |
| 10.3390/v17101343 | Aloisio et al 2025 | `NA` | `SARS2` | Dan | 
| 10.1093/imammb/14.2.85 | Hughes et al 1997 | `NA` |  | `Plants` | Ellen |

Count = 15

## DAI = Data already included
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | By | DOI of authoritative paper |
|:---|:---|:---:|:---:|:---:|:---|:---|
| 10.1101/2025.02.01.636082v1 | Eales et al 2025 | `DAI` | `H5N1` | | Ellen | 10.1038/s41586-024-07849-4 |
| 10.1101/2025.02.01.636082v1 | Eales et al 2025 | `DAI` | `H5N1` | | Ellen | 10.1038/s41586-024-08166-6 |
| 10.1101/2025.02.01.636082v1 | Eales et al 2025 | `DAI` | `H5N1` | | Ellen | 10.1038/s41586-024-08063-y |
| 10.1371/journal.pbio.3001333 | Kissler 2021 PLOS CtTrajectories | `DAI` | `SARS2` | | Ellen | 10.1038/s41467-023-41941-z |
| 10.1056/nejmc2102507 | Kissler 2021 NEJM CtTrajectories_B117 Vax | `DAI` | `SARS2` | | Ellen | 10.1038/s41467-023-41941-z |
| 10.7554/eLife.81849 | Hay Kissler 2022 eLife SC2 kinetics | `DAI` | `SARS2` | | Ellen | 10.1038/s41467-023-41941-z |
| 10.1056/nejmc2102507 | Kissler et al 2021 | `DAI` | `SARS2` | | Ellen RR | 10.1038/s41467-023-41941-z |
| 10.1371/journal.pbio.3001333 | Kissler et al 2021 | `DAI` | `SARS2` | | Ellen RR | 10.1038/s41467-023-41941-z |
| 10.1016/s1473-3099(21)00648-4 | Singanayagam et al 2021 | `DAI` | `SARS2` | | Ellen RR | 10.1016/S2213-2600(22)00226-0 |
| 10.1371/journal.pcbi.0030240 | Handel et al 2007 | `DAI` | `Flu` | | Ellen RR | 10.1086/314938 |

Count = 10

Total tally = 145
