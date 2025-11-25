# Convert raw data files to useable for OPKC
library(jsonlite)
library(data.table)

path <- "/data/jones2021_rawfiles/min-3-timeseries.json"

# Most comprehensive data stored in min-3-timeseries.json
raw <- fromJSON(path, simplifyVector = FALSE)
people <- raw$people

if (is.data.frame(people)) {
  people <- lapply(seq_len(nrow(people)), function(i) {
    row <- people[i, ]
    lapply(row, function(x) if (is.list(x)) x[[1]] else x) # convert each row (which is a one-row data.frame) to a simple list
  })
}
# avoid issues with JSON date formatting
safe_date <- function(x) {
  if (is.null(x)) return(NA_character_)
  x <- unlist(x)
  if (!is.character(x)) x <- as.character(x)
  x
}

# each personHash becomes rows with each measurement
people_dt <- rbindlist(lapply(people, function(p) {
  d   <- safe_date(p$date)
  vl  <- unlist(p$viralLoad)
  age <- unlist(p$age)
  tn  <- unlist(p$testName)
  tc  <- unlist(p$testCentre)
  tcc <- unlist(p$testCentreCategory)
  n <- length(d)

  data.table(
    personHash = rep(p$personHash, n),
    gender = rep(p$gender, n),
    PAMS1 = rep(p$PAMS1, n),
    hospitalized = rep(p$hospitalized, n),
    onset = rep(if (is.null(p$onset)) NA else p$onset, n),
    B117 = rep(p$B117, n),
    date = as.IDate(d),
    viralLoad = as.numeric(vl),
    age = as.numeric(age),
    testName = tn,
    testCentre = tc,
    testCentreCategory = tcc
  )
}), fill = TRUE)

write.csv(people_dt, "jones2021.csv", row.names = FALSE)
