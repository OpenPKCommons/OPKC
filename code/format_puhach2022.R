library(readxl)

path <- "/data/puhach2022.xlsx"

puhach2022 <- read_excel(path, sheet = 1)

write.csv(puhach2022, "puhach2022.csv", row.names = FALSE)