# epl-stats

A simple python tool to get (`get.py`) player stats for all players and seasons from the [official Premier League website](http://premierleague.com/). The stats obtained are:

| column name        | desc           |
| ------------|----------------|
| id | Unique to the player on the website |
| name | Th player's name |
| position | Goalkeeper, Defender, Midfielder, or Forward |
| nationality | The nation they choose to represent |
| clubs | List of Premier League clubs they have played for |
| seasons | List of seasons they have played in the Premier League |
| num_of_seasons | The total number of seasons played in the Premier League |
| apps | The number of Premier League appearances |
| wins | The number of Premier League wins |
| losses | The number of Premier League losses |
| clean_sheets | The number of Premier League clean sheets |
| assists | The number of Premier League assists |
| goals | The number of Premier League goals |

More to be added in due course. For now, the complete data set is available under `data/all.csv`. 