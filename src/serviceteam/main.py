#!/usr/bin/env python
from serviceteam.crew import ServiceteamCrew

def run():
    # Input query from the user
    user_query = input("Please enter your query: ")

    inputs = {
        'Query': user_query
    }
    response = ServiceteamCrew().crew().kickoff(inputs=inputs)
    print(response)
