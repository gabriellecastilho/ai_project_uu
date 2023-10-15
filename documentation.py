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

create_transition_matrix.__doc__ = """
Description
-----------
This function is used to create a transition matrix that models the probability of the user's 
transition from one place category to another. The transition matrix is calculated based on
user's historical data and probabilities associated with visiting different place category.  

Arguments
-----------
user            The unique identifier of the user for whom the transition matrix is created.
main_table      The main table containing user reviews, location details, and relevant
                attributes for tourism places in Indonesia.

Returns
------------
This function returns a Pandas DataFrame, transition_matrix, representing the probabilities
of the transition from one place category to another.
"""

recommend_category.__doc__ = """
Description
-----------
This function is used to recommend the new category according to the user's current category
interest. it takes into account the transition probabilities within the matrix for the suggestion
of the new category that the user may find interesting.

Arguments
---------
user                The unique identifier of the user for whom the category recommendation is generated.
category            The current category that the user is interested in.
transition_matrix   A Pandas DataFrame containing the transition matrix generated by create_transition_matrix function.

Returns
-------
This function returns the new category recommended for the user to explore.
"""  

create_rating_by_age_table.__doc__ = """
Description
-----------
This function is used to create the rating_by_age table, which aggregates and calculates the average rating
of places for the specific city, by user age range.

Arguments
---------
city            The name of the city for which rating age table generated.
main_table      The main table generated by the function create_main_table.

Returns
--------
The function returns a Pandas DataFrame rating_by_age_table which containg the average rating of places for 
a specific city, categorised by user age group.
"""  

create_user_history.__doc__= """
Description
-----------
This function is used to create a user_history list based on the places visited
by a specific user.

Arguments
---------
user            The unique identifier of the user for whom the visited history retrived.
main_table      The main table  generated by the function create_main_table.

Returns
-------
This function return a list with the ids of places visited by a specific user. In case of
no history, an empty list is returned.
"""

recommend_place.__doc__= """
Description
-----------
This function is used to recommend places based on the user unique identifier, user age range,
among other characteristics.

Arguments
---------
user            The unique identifier of the user for whom the recommendation is generated
category        The category for which user looking for recommendation.
city            The city for which recommendations are made.
main_table      The main table generated by the function create_main_table.
rating_by_age   rating_by_age table created by create_rating_by_age_table function.
user_history    The list of place_Id based on user visited history.

Returns
--------
This function returns a dictionary with the recommended places, where the key is the id
and the value is the name.
"""

run_program.__doc__= """
Description
-----------
This function calls all the functions previously defined to run the program.

Arguments
---------

user            The unique identifier user for whom seeking for place recommendation.
main_table      The main table generated by the function create_main_table.
category        The initial category of interest of the user.
city            The name of the city for which recommendations are provided.

Returns
--------
The function returns the recommended category in as a tuple with the recommendations generated by
the function recommend_place.
"""