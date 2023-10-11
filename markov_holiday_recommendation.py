import pandas as pd
import numpy as np
from itertools import permutations
from itertools import combinations_with_replacement

def create_main_table():

    # Loading datasets
    locations = pd.read_csv("https://raw.githubusercontent.com/gabriellecastilho/datasets/master/indonesia_tourism.csv")
    ratings = pd.read_csv("https://raw.githubusercontent.com/gabriellecastilho/datasets/master/indonesia_tourism_rating.csv")
    users = pd.read_csv("https://raw.githubusercontent.com/gabriellecastilho/datasets/master/indonesia_tourism_user.csv")

    # Merging / Joining datasets
    main_table = pd.merge(ratings, users, on='User_Id', how='inner')
    main_table = pd.merge(main_table, locations, on="Place_Id", how="inner")

    # Dropping duplicates
    main_table = main_table.drop_duplicates()

    # Creating column "Age Range"
    main_table["Age_Range"] = pd.cut(main_table['Age'], bins=[0, 17, 25, 35, 50, 65, 100], labels=['0-17', '18-25', '26-35', '36-50', '51-65', '65+'])

    # Selecting only relevant attributes
    main_table = main_table[["User_Id", "Age", "Age_Range", "Place_Id", "Place_Name", "Category", "City", "Place_Ratings", "Rating", "Price"]]

    # Sorting values by user id and ratings
    main_table = main_table.sort_values(by=["User_Id", "Place_Ratings", "Rating"], ascending=[True, False, False])

    # Reordering table index
    main_table = main_table.reset_index(drop=True)

    # Translating categories to English
    def translate_category(item):
        if item == "Taman Hiburan": return "Amusement Park"
        elif item == "Tempat Ibadah": return "Place of Worship"
        elif item == "Budaya": return "Culture"
        elif item == "Cagar Alam": return "Natural Reserve"
        elif item == "Bahari": return "Nautical"
        elif item == "Pusat Perbelanjaan": return "Shopping Center"

    main_table["Category"] = main_table[["Category"]].applymap(translate_category)

    return main_table

def create_probability_table(user, main_table):

    # Case when a new user doesn't have a history
    if user not in main_table["User_Id"].unique():

        # Creating dataframe with equal probabilities
        prob_table = pd.DataFrame()
        prob_table["Category"] = main_table["Category"].unique()
        prob_table["Probability"] = 1 / prob_table.shape[0]
    
    else:

        # Filtering main table by target user
        user_table = main_table[main_table["User_Id"] == user]

        # Creating dataframe with user history category count and average rating
        prob_table = pd.DataFrame()
        prob_table["Count"] = user_table["Category"].value_counts()
        prob_table["Avg_Rating"] =  user_table.groupby("Category")["Place_Ratings"].mean()
        prob_table.reset_index(inplace=True)
        prob_table = prob_table.rename(columns = {'index':'Category'})

        # Calculating weighted count sum of places visited by rating
        weighted_sum = (prob_table["Avg_Rating"] * prob_table["Count"]).sum()

        # Creating and calculating column "Probability" for each category
        prob_table["Probability"] = (prob_table["Count"] * prob_table["Avg_Rating"]) /  weighted_sum

    return prob_table

def create_transition_matrix(user, main_table):

    # Calling the function create_probability_table for the categories the user has visited
    prob = create_probability_table(user, main_table)

    # Creating the categories transitions for the transition matrix
    perm = list(permutations(prob["Category"].unique(), 2))
    comb = list(combinations_with_replacement(prob["Category"].unique(), 2))
    transition_matrix = pd.DataFrame(data = perm + comb, columns = ("Category_1", "Category_2"))
    transition_matrix = transition_matrix.drop_duplicates().reset_index(drop=True)

    # Calculating the probability of a user to visit a category based on the category of the page he is seeing at the moment
    def probability(row):
        prob1 = prob["Probability"][prob["Category"] == row[0]].iloc[0]
        prob2 = prob["Probability"][prob["Category"] == row[1]].iloc[0]
        return prob1 * prob2 / prob1

    transition_matrix["Probability"] = transition_matrix.apply(probability, axis=1)

    return transition_matrix

def recommend_category(user, category, transition_matrix):

    # Selecting a new category based on the transition matrix probabilities
    new_category = np.random.choice(transition_matrix["Category_2"][transition_matrix["Category_1"] == category].values,
                                replace=True,
                                p=transition_matrix["Probability"][transition_matrix["Category_1"] == category].values)
    return new_category

def create_rating_age_table(city, main_table):

    # Filtering places by target city
    places_by_city = main_table[main_table["City"] == city]

    # Selecting the necessary columns and calculating the average rating by age range
    rating_age = places_by_city[["Age_Range", "Place_Id", "Place_Name", "Category", "Place_Ratings"]].groupby(["Age_Range", "Category",  "Place_Id", "Place_Name"]).mean().dropna()

    # Ranking best places by rating
    rating_age = rating_age.sort_values(["Age_Range", "Place_Ratings"], ascending=[True, False])
    rating_age.reset_index(inplace=True)

    return rating_age

def create_user_history(user, main_table):

    # Case when the user doesn't have a history
    if user not in main_table["User_Id"].unique():
        return []

    else:

        # Listing the id of places visited by users
        def list_locations(row):
            return list(row['Place_Id'])

        user_history = main_table.groupby('User_Id').apply(list_locations)

        # Returning only the id of places visited by target user
        return user_history[user]

def recommend_place(user, category, city, main_table, rating_age, user_history):

    # Case when user doesn't have a history
    if user not in main_table["User_Id"].unique():

        # Filtering main table by category and city
        options = main_table[(main_table['Category'] == category) & (main_table["City"] == city)]

        # Calculating average user ratings for all age ranges
        options = options.groupby(["Place_Id", "Place_Name"])["Place_Ratings"].mean()
        options.sort_values(axis=0,ascending=False)

        # Selecting best rated place
        top_place = options.nlargest(1, keep='all')

        # Getting the Place_Id and Place_Name
        place_id = top_place.index[0][0]
        place_name = top_place.index[0][1]

    else:

        # Finding the user's age range
        age_range = main_table["Age_Range"][main_table["User_Id"] == user].iloc[0]

        # Selecting options from the same age range
        options = rating_age[rating_age["Age_Range"] == age_range]

        # Selecting best places from the category recommended
        options = options[options["Category"] == category]
        options = list(options["Place_Id"])

        # Recommending best ranked place from that category and age range
        place_id = options[0]

        # Calculate user average spending history for the category
        avg_spending = main_table["Price"][main_table["User_Id"] == user][main_table["Category"] == category].mean()

        # Finding the price for the first recommendation
        place_price = main_table["Price"][main_table["Place_Id"] == place_id].iloc[0]

        # Checking if the user already visited the place or if it's too expensive, if so, recommends the next place
        while (place_id in user_history) or (place_price > 2 * avg_spending):
            options.pop(0)
            place_id = options[0]
            place_price = main_table["Price"][main_table["Place_Id"] == place_id].iloc[0]

        # Find place name
        place_name = main_table["Place_Name"][main_table["Place_Id"] == place_id].iloc[0]

    # Returning id and name for recommended place
    return(place_id, place_name)

if __name__ == "__main__":

    # Creating main table
    main_table = create_main_table()

    # Defining target user, city, and category of the page originating the recommendation
    # Example: User 1 is visiting the page of a museum (culture) in Jakarta

    available_users = main_table["User_Id"].unique()
    user = int(input(f"""Add User ID ({available_users.min()} to {available_users.max()}): """))
    if user not in available_users:
        print(f"""User {user} is new. No history found.""")

    available_categories = main_table["Category"].unique()
    category = input(f"""Add Category ({", ".join(available_categories)}): """)
    while category not in available_categories:
        category = input(f"""Category not found.\nAdd Category ({", ".join(available_categories)}):""")

    available_cities = main_table["City"].unique()
    city = input(f"""Add City ({", ".join(available_cities)}): """)
    while city not in available_cities:
        city = input(f"""City not found.\nAdd City ({", ".join(available_cities)}):""")
        
    # Creating transition matrix for target user
    transition_matrix = create_transition_matrix(user, main_table)

    # Recommending a category for target user
    category = recommend_category(user, category, transition_matrix)

    # Creating table with places ranking by age range
    rating_age = create_rating_age_table(city, main_table)

    # Creating list with places visited by target user
    user_history = create_user_history(user, main_table)

    # Recommending best ranked places from category, given that user hasn't visited it yet
    place_id, place_name  = recommend_place(user, category, city, main_table, rating_age, user_history)

    # Printing recomendation category and place name
    print(f"""{category}:  {place_name}""")