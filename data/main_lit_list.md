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


## Literature List
### Datasets already downloaded (ingested) and formatted (digested)
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | By |
|:---|:---|:---:|:---:|:---:|---:|
| 10.1038/s41564-022-01105-z | Ke et al 2022 Daily | `DIGESTED` | `SARS2` | | Stephen |
| 10.1038/s41467-023-41941-z | Kissler et al 2023 | `DIGESTED` | `SARS2` | | Stephen |
| 10.1371/journal.pbio.3002463 | Russell et al 2024 | `DIGESTED` | `SARS2` | | Stephen |
| 10.1126/sciimmunol.adj9285 | Wagstaffe et al 2024 | `DIGESTED` | `SARS2` | | Carrie |
| 10.1016/S1473-3099(24)00183-X | Wongnak et al 2024 | `DIGESTED` | `SARS2` | | Stephen |
| 10.1016/S2213-2600(22)00226-0 | Hakki et al 2022 | `DIGESTED` | `SARS2` | `VAX` `LAB`| Oliver | [github](https://github.com/HPRURespMed/SARS-CoV-2-viral-shedding-dynamics) |
| 10.1128/jcm.01785-21 | Savela Winnett Romano et al 2022 | `Ingesting` | `SARS2` | | Oliver | [author site](https://data.caltech.edu/records/bv2tf-aap55) |

Count = 7

### DE = DATA EXISTS (in priority order)
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | INGEST-IN-PROGRESS-BY? | Data link |
|:---|:---|:---:|:---:|:---:|:---|:---|
| 10.1101/2025.02.01.636082v1 | Eales et al 2025 | `DE` | `H5N1` | | Ellen | [github](https://github.com/Eales96/H5N1_viral_kinetics) |
| 10.1038/s41564-024-01668-z | Waickman et al 2024 | `DE` | `Dengue` | `LAB` | UNCLAIMED | [data at paper](https://www-nature-com.colorado.idm.oclc.org/articles/s41564-024-01668-z) |
| 10.7554/eLife.92606.3 | Vuong et al 2024 | `DE` | `Dengue` | `LAB` | UNCLAIMED | [github](https://github.com/Nguyenlamvuong/Dengue_Viremia_Kinetics_eLife_2024/blob/main/Viremia%20and%20outcomes%20240522.Rdata) |
| 10.7326/M20-1495 | Kucirka et al 2020 | `DE` | `SARS2` | `MA` | UNCLAIMED | [github](https://github.com/HopkinsIDD/covidRTPCR) |
| 10.1038/s41591-022-01816-0 | Puhach et al 2022 | `DE` | `SARS2` | | Carrie | [Extended data at paper](https://www-nature-com.colorado.idm.oclc.org/articles/s41591-022-01816-0#Sec18) |
| 10.1126/science.abi5273 | Jones et al 2021 | `DE` | `SARS2` | | Carrie | [github](https://github.com/VirologyCharite/SARS-CoV-2-VL-paper/tree/main) |
| 10.1038/s41467-020-20568-4 | van Kampen et al 2021 | `DE` | `SARS2` | `LAB` | UNCLAIMED | [Source data at paper](https://www-nature-com.colorado.idm.oclc.org/articles/s41467-020-20568-4#Sec12) |
| 10.1101/2025.07.02.662782 | Alahakoon et al 2025 Tracking West Nile | `DE` | `WestNile` | `mosq` `birds` | UNCLAIMED | [github](https://github.com/PunyaAlahakoon/west_nile_virus_abm/tree/main/3_figure_generation/data) |
| 10.1038/s41467-025-61553-z | Peña-Mosca et al 2025  | `DE` | `Flu` |`H5N1` `cows` | Ellen | [github](https://github.com/fepenamosca/hpai_impact_dairies/tree/fd5f303f4aae47ef3a6259e7e7b94284f8c3af67/data) |
| 10.1038/s41564-025-01998-6 | Facciuolo et al 2025 | `DE` | `Flu` |`H5N1` `cows` | Ellen | [Source Data at paper](https://www-nature-com.colorado.idm.oclc.org/articles/s41564-025-01998-6#Sec25) |
Count = 10

### DE-NEA = Data exists, not easily accesible (alphabetized)
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | AUTHOR_CONTACTED? |
|:---|:---|:---:|:---:|:---:|---:|
| 10.1007/s40121-025-01235-x | Berger et al 2025 | DE-NEA | `SARS2` |  | No |
| Preprint | Blanquart et al 2021 | DE-NEA | `SARS2` |  | No |
| 10.1056/nejmc2202092 | Boucau et al 2022 | DE-NEA | `SARS2` | `Omicron` `sx` | On deck |
| 10.1093/aje/kwm375 | Carrat et al 2008 | DE-NEA | `Flu` | `H1N1` `sx` | On deck |
| 10.1016/s2666-5247(20)30172-5 | Cevik et al 2020 | DE-NEA | `SARS2` `SARS` `MERS` | `MA` `REF` | No |
| 10.7326/0003-4819-151-7-200910060-00142 | Cowling et al 2009 | DE-NEA | `Flu` | `H1N1` | On deck |
| 10.1098/rsif.2016.0289 | Hadjichrysanthou et al 2016 | DE-NEA | `Flu` | `H1N1` | On deck |
| 10.1038/s41591-020-0869-5 | He et al 2020 | DE-NEA | `SARS2` |  | No |
| 10.1038/s41591-022-01780-9 | Killingley et al 2022 | DE-NEA | `SARS2` | `sx` `LAB` | On deck |
| 10.1016/j.antiviral.2004.04.005 | Lee et al 2004 | DE-NEA | `RSV` | `sx` | No |
| 10.1093/biostatistics/kxaa009 | Mahsin et al 2019 | DE-NEA | `Flu` | `H1N1` `MOSP` | No |
| 10.1038/s44298-025-00132-x | Mehta et al 2025 | DE-NEA | `SARS` `Flu` `RSV` | `H3N2` | No |
| 10.1128/iai.29.2.348-355.1980 | Murphy et al 1980 | DE-NEA | `Flu` | `H1N1` | No |
| 10.1016/j.antiviral.2020.104763 | Sloan et al 2020 | DE-NEA | `Flu` | `XS` `H1N1` | On deck |
| 10.1001/jamanetworkopen.2021.42796 | Stankiewicz et al 2022 | DE-NEA | `SARS2` |  | No |
| 10.1038/s41586-020-2196-x | Wolfel et al 2020 | DE-NEA | `SARS2` |  | No |
| 10.3389/fmicb.2019.02342  | Yuko Sakai-Tagawa et al 2019 | DE-NEA | `Flu` | `H1N1` `H3N2` `H5N1` `H5N6` `H7N9` `Victoria` `Yamagata` | No |
Count = 17

### DME = Data MAY exist
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

Count = 40

### IDed paper in scanning queue
| DOI | PaperNameString | Status/Classification | Pathogen | Tags | By |
|:---|:---|:---:|:---:|:---:|---:|
| 10.1016/S2666-5247(23)00005-8 | Galmiche et al 2023 | `IDed` | | Ellen |
| 10.1016/S2666-5247(23)00101-5 | Zhou et al 2023 | `IDed` | | Ellen |
| 10.3389/fimmu.2018.00323 | Ascough et al 2018 | `IDed` | | Ellen |
| 10.1007/82_2022_257 | Dayananda et al 2022 | `IDed` | | Ellen |
Count = 4+
*Check with Ellen for the most complete queue*

### MO = Modeling Only papers
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
Count = 14

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
Count = 14

### DAI = Data already included
| DOI | PaperNameString | Status/Classification | Tags | By | DOI of authoritative paper |
|:---|:---|:---:|:---:|:---|:---|
| 10.1038/s41586-024-07849-4 | Caserta et al 2025 | `DAI` | | Ellen | 10.1101/2025.02.01.636082v1 |
| 10.1038/s41586-024-08166-6 | Baker et al 2024 | `DE` | | Ellen | 10.1101/2025.02.01.636082v1 |
| 10.1038/s41586-024-08063-y | Halwe et al 2024 | `DE` | | Ellen | 10.1101/2025.02.01.636082v1 |
| 10.1371/journal.pbio.3001333 | Kissler 2021 PLOS CtTrajectories | `DAI` | | Ellen | 10.1038/s41467-023-41941-z |
| 10.1056/nejmc2102507 | Kissler 2021 NEJM CtTrajectories_B117 Vax | `DAI` | | Ellen | 10.1038/s41467-023-41941-z |
| 10.7554/eLife.81849 | Hay Kissler 2022 eLife SC2 kinetics | `DAI` | | Ellen | 10.1038/s41467-023-41941-z |
| 10.1056/nejmc2102507 | Kissler et al 2021 | `DAI` | | Ellen RR | 10.1038/s41467-023-41941-z |
| 10.1371/journal.pbio.3001333 | Kissler et al 2021 | `DAI` | | Ellen RR | 10.1038/s41467-023-41941-z |
| 10.1016/s1473-3099(21)00648-4 | Singanayagam et al 2021 | `DAI` | | Ellen RR | 10.1016/S2213-2600(22)00226-0 |
| 10.1371/journal.pcbi.0030240 | Handel et al 2007 | `DAI` | | Ellen RR | 10.1086/314938 |
Count = 10

Total tally = 109
