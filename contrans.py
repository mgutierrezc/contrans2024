import numpy as np
import pandas as pd
import os, dotenv, requests, json

dotenv.load_dotenv()

class contrans:
    def __init__(self):
        """
        Initializes the class instance.
        Attributes:
            mypassword (str): The password retrieved from the environment variable 'mypassword'.
        """

        self.mypassword = os.getenv("mypassword")
        self.congresskey = os.getenv("congresskey")
        self.newskey = os.getenv("newskey")

    def get_votes(self):
        """
        Get the 118th House of Representatives voting data

        This function will return a datafme of the 118th House of Representatives voting data.
        The dataframe will contain the following columns:

        congress: The number of the congress
        chamber: The chamber of congress
        rollnumber: The roll number of the vote
        icpsr: The ICPSR number of the voter
        cast_code: The cast code of the vote
        prob: The probability of the voter's vote for the bill
 
        
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
    
    def get_useragent(self):
        url = "https://httpbin.org/user-agent"
        r = requests.get(url)
        user_agent = json.loads(r.text)["user-agent"]
        return user_agent

    def make_headers(self, email="jkropko@virginia.edu"):
        useragent = self.get_useragent()
        headers = {
            "User-Agent": useragent,
            "From": email
        }
        return headers

    def get_bioguideIDs(self, query="covid"):
        params = {"api_key": self.congresskey}
        headers = self.make_headers()
        root = "https://api.congress.gov/v3"
        endpoint = "/member"
        r = requests.get(root + endpoint, 
                            params=params, 
                             headers=headers)
        bio_df = pd.json_normalize(r.json(),
                                    record_path=["members"])
        return bio_df[["name", "state", "district", "bioguideId"]]