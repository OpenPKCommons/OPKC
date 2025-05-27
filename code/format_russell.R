library(tidyverse) 

obs <- as_tibble(readRDS("data/russell2024.rds"))

write_csv(obs, file="data/russell2024.csv")