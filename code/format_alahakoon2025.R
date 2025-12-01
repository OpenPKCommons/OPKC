# From /data/Alahakoon2025_rawfiles 

# ct vals contained in the following:
# 1. NE_WNV_Positive_22_23_24
# agency_code	agency_pool_num	surv_year	site_name	calculated_county	calculated_state	longitude	latitude	collection_date	disease_week	trap_type	lure	species	sex_condition	num_count	WNV	ctval
# 2. Nebraska_Mosquito_Pool_Data_22_23_24
# agency_code,agency_pool_num,surv_year,site_name,calculated_county,calculated_state,longitude,latitude,collection_date,disease_week,trap_type,lure,species,sex_condition,num_count,WNV,ctval
# 3. sample_sizes_by_surveil_calc
# surv_year	disease_week	species	pool_size	WNV	ctval	state

library(dplyr)

NE1 <- read.csv("/data/alahakoon2025_rawfiles/NE_WNV_Positive_22_23_24.csv")
NE2 <- read.csv("data/alahakoon2025_rawfiles/Nebraska_Mosquito_Pool_Data_22_23_24.csv")
sample <- read.csv("/data/alahakoon2025_rawfiles/sample_sizes_by_surevil_calc.csv")

# only want where WNV present - confirm 1 is max value representing only 1 mosq with WNV
# max_value_NE1 <- max(NE1$WNV, na.rm = TRUE)
# print(max_value_NE1)
# max_value_NE2 <- max(NE2$WNV, na.rm = TRUE)
# print(max_value_NE2)
# max_value_sample <- max(sample$WNV, na.rm = TRUE)
# print(max_value_sample)

# select only where WNV = 1
NE1 <- NE1[NE1$WNV == 1, ]
NE2 <- NE2[NE2$WNV == 1, ]
sample <- sample[sample$WNV == 1, ]

combined_nebraska <- rbind(NE1,NE2)
#print(combined_nebraska)
combined_nebraska_reduced <- combined_nebraska %>%
  select(surv_year, disease_week, species, num_count, WNV, ctval, calculated_state)
#print(combined_nebraska_reduced)
combined_nebraska_reduced <- combined_nebraska_reduced %>%
  rename(
    pool_size = num_count,
    state = calculated_state
  )

sample_reduced <- sample %>%
  select(surv_year, disease_week, species, pool_size, WNV, ctval, state)

alahakoon2025 <- rbind(combined_nebraska_reduced,sample_reduced)
print(alahakoon2025)

write.csv(alahakoon2025, file = "/data/alahakoon2025.csv", row.names = FALSE)
