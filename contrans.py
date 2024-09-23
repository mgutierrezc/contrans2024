import numpy as np
import pandas as pd
import os

class contrans:
    def __init__(self):
        """
        Initializes the class instance.
        Attributes:
            mypassword (str): The password retrieved from the environment variable 'mypassword'.
        """

        self.mypassword = os.getenv("mypassword")

    def get_votes(self):
        """
        Fetches voting data from a specified URL and returns it as a pandas DataFrame.
        Returns:
            pandas.DataFrame: A DataFrame containing the voting data from the specified URL.
        """

        url = "https://voteview.com/static/data/out/votes/H118_votes.csv"
        votes = pd.read_csv(url)
        return votes
    
    def get_ideology(self):
        """
        Fetches ideology data from a specified URL and returns it as a pandas DataFrame.
        Returns:
            pandas.DataFrame: A DataFrame containing the ideology data from the specified URL.
        """

        url = "https://voteview.com/static/data/out/members/H118_members.csv"
        ideology = pd.read_csv(url)
        return ideology