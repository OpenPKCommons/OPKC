library(readxl)

path <- "/data/vanKampen2021.xlsx"

vanKampen2021 <- read_excel(path, sheet = 1)

write.csv(vanKampen2021, "vanKampen2021.csv", row.names = FALSE)