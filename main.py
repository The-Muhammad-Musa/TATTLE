""""
TATTLE: Targeted Anti-Target Telegram, Lmao Edition

A script written by Hesskin Empire (with help from github copilot) to target a specific region
for manual recruitment in nationstates.
"""

# Going to do my best to properly comment it this time :3 (AKA I will annotate this like I am teaching you python <3)

# First we need to import requests, etree and time
import requests as req
import xml.etree.ElementTree as ET
import time


# We need to create the canonicalize function which will replace spaces with underscores and lowercase all letters
def canonicalize(string: str):
    return string.replace(" ", "_").lower()


# Next we need to gather the User's main nation through a string input function and canonicalize it
user_nation = str(input("Please enter your main nation: "))
user_nation_c = canonicalize(user_nation)

# Now we are creating our headers
headers = {
        'User-Agent': f'TATTLE/0.1; Developed by nation=hesskin_empire in use by nation={user_nation_c}'}

# Greet the user and ask for their target region and canonicalize it
target_region = str(input(f"Hello {user_nation}, welcome to TATTLE. Please enter your target region: "))
target_region = canonicalize(target_region)

# Ask if the user wants to enter WA only mode or not
wa_only = str(input("Would you like to enter WA only mode? (y/n): ")).lower()

while wa_only not in ['y', 'n']:
    print(f"I am sorry, {user_nation} but {wa_only} is not a valid entry. Please try again! :3")
    wa_only = str(input("Would you like to enter WA only mode? **(y/n)**: ")).lower()

# Checking if wa_only is y or n, if y it sets wa_only to True, if n then it sets it to False
if wa_only == 'y':
    wa_only = True
else:  # We know it is either y or n because of our while loop up there
    wa_only = False

# Ask the user for their template in a string input
template = str(input("Please enter your recruitment telegram template: "))

# Now we are going to open a request to the nationstates region API for the target region
regions_nations = req.get(f"https://www.nationstates.net/cgi-bin/api.cgi?region={target_region}&q=nations",
                          headers=headers)

# Now we create the region_officers variable and request the region officers from the nationstates API
region_officers = req.get(f"https://www.nationstates.net/cgi-bin/api.cgi?region={target_region}&q=officers",
                          headers=headers)

# Now we are going to isolate the nations from the <NATIONS> header in the XML using ETree
regions_nations = ET.fromstring(regions_nations.content).find("NATIONS")

# Now we pull all the different <OFFICER> tags out of <OFFICERS>
region_officers = ET.fromstring(region_officers.content).find("OFFICERS").findall("OFFICER")

# Now we take the officers in region_officers and find all the <NATION>
region_officers = [officer.find("NATION").text for officer in region_officers]

# Now we break the regions_nations variable into a list of nations, which are separated by ':' right now
regions_nations = regions_nations.text.split(":")

# Now we need to use list comprehension to iterate through the regions_nations list and remove the region_officers
regions_nations = [nat for nat in regions_nations if nat not in region_officers]

if wa_only:
    # Grab the WA nations from the region using the wanations shard
    wa_nations = req.get(f"https://www.nationstates.net/cgi-bin/api.cgi?region={target_region}&q=wanations",
                         headers=headers)

    # Go ahead and separate the wa nations into a list
    wa_nations = ET.fromstring(wa_nations.content).find("UNNATIONS").text.split(",")

    # Now we are going to iterate through again and make it WA only if wa_only is True
    regions_nations = [nat for nat in regions_nations if nat in wa_nations]

# We are just going to give it a cheeky little new line to make it look nicer
print("\n")

# Now we just need to iterate through the regions_nations list and print out groups of 8 every 8 seconds
for i in range(0, len(regions_nations), 8):
    print(", ".join(regions_nations[i:i+8]))
    print(f'{template}\n')
    time.sleep(50)
