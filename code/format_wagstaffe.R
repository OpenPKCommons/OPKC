library(tidyverse) 

wagstaffe2024_nose <- read_csv("data/wagstaffe2024_nose.csv")
wagstaffe2024_throat <- read_csv("data/wagstaffe2024_throat.csv")

format_wagstaffe <- function(df){
	df %>% 
		pivot_longer(-PersonID, names_to="DaysPostInoculation", values_to="GEml") 
}

wagstaffe2024_combined <- bind_rows(
	mutate(format_wagstaffe(wagstaffe2024_nose),site="nose"),
	mutate(format_wagstaffe(wagstaffe2024_throat),site="throat")
	)

write_csv(wagstaffe2024_combined, file="data/wagstaffe2024.csv")