### load packages
pak::pak(c("httr2", "tidyverse", "rvest", "janitor", "jsonlite", "httr"))

library(jsonlite)
library(httr2)
library(tidyverse)
library(rvest)
library(janitor)


### scrape gemeinden

# specify the URL of the Wikipedia page
url_gemeinde <- "https://de.wikipedia.org/wiki/Liste_Schweizer_Gemeinden"

# send a GET request to the URL
gemeinden <- httr2::request(url_gemeinde) %>%
  httr2::req_perform() %>%
  httr2::resp_body_html() %>%
  rvest::html_nodes("table.wikitable") %>%
  rvest::html_table() %>%
  purrr::chuck(1) %>%
  janitor::clean_names() %>%
  dplyr::select(offizieller_gemeindename, kanton, bfs_nr)

### write Gemeinden
write_csv(gemeinden, file = "data/gemeinden.csv")

### scrape Feiertage


response <- httr2::request(holiday_url) %>%
  req_url_query(
    countryIsoCode = "CH",
    languageIsoCode = "DE",
    validFrom = "2022-01-01",
    validTo = "2022-12-31"
  ) %>%
  req_perform() %>%
  resp_body_json(check_type = FALSE)




df_feiertage <- purrr::map_dfr(response, function(x) {
  unlist(x)
})

### clean Feiertage
clean_feiertage <- df_feiertage %>%
  clean_names() %>%
  tidyr::unite(canton,
               starts_with("subdivisions_short_name"),
               sep = ", ",
               na.rm = T) %>%
  select(id, start_date, end_date, name_text, nationwide, canton)

### save Feiertage
write_csv(clean_feiertage, file = "data/feiertage.csv")
