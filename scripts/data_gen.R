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

### scrape Ferien


response <- httr2::request(holiday_url) %>%
  req_url_query(
    countryIsoCode = "CH",
    languageIsoCode = "DE",
    validFrom = "2022-01-01",
    validTo = "2022-12-31"
  ) %>%
  req_perform() %>%
  resp_body_json(check_type = FALSE)

json_content <- jsonlite::content(response, as = "text")
parsed_json <- jsonlite::fromJSON(json_content)
