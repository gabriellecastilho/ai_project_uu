from top5_markov_holiday_recommendation import *
from test_cases import *

create_main_table.__doc__ = """
Description
-----------
This function is used to create a consolidated main table by loading and merging
multiple datasets related to tourism in Indonesia. The resulting table provides a
comprehensive view of user reviews, location details, and additional attributes
for tourism places in Indonesia.

Returns
-------
The function returns a Pandas DataFrame, which is the consolidated main table
containing user reviews, location details, and relevant attributes for tourism
places in Indonesia.
"""

create_probability_table.__doc__ = """
Description
-----------
This function is used to create a probability table that calculates the likelihood
of a user with a given history to visit places of various categories in Indonesia.
The probability table is generated based on user historical data and place category ratings.

Arguments
---------
user            The unique identifier of the user for whom the probability table is created.
main_table      The main table containing user reviews, location details, and relevant
                attributes for tourism places in Indonesia.

Returns
-------
The function returns a Pandas DataFrame, user_probability_table, containing information
about the user's historical visits, category counts, average ratings, and the calculated
probabilities for visiting places in different categories.
"""