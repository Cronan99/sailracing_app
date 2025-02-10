from bs4 import BeautifulSoup
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Boat_type
import os


URL = "https://www.batsidan.com/batar/srs-tal.php"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
boats = soup.find_all("td")

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'sailracing.db')
engine = create_engine(f"sqlite:///{db_path}")
session = sessionmaker(bind=engine)
session = session()

def get_srs():
    # Using given URL gets all boats srs-number and creates a list.
    # The list contains structure of 1:boattype, 2:SRS, 3:SRS, 4:SRS, 5:SRS followed by next boat.
    boat_list = []
    # Boattype, SRS, SRS_No, SRS_S/H, SRS_S/H_No
    for boat in boats:
        boat_list.append(boat.text)    
    return boat_list

def create_boat_objects():
    # Add all boats/data that has been scraped to the database

    boats = get_srs()

    # the list with boats contain a continous array with name, srs, srs, srs, srs followed by the next boat
    for i in range(0, len(boats), 5):
        name = boats[i]         # Boat name
        srs = boats[i+1]        # SRS
        srs_ns = boats[i+2]
        srs_sh = boats[i+3]
        srs_sh_ns = boats[i+4]

        boat_exist = session.query(Boat_type).filter_by(name=name).first()

        if not boat_exist:
        # Only if the boat doesnt exist it gets added to eliminate the occourence of doubles
            create_boat = Boat_type(
                name=name,
                srs=srs,
                srs_ns=srs_ns,
                srs_sh=srs_sh,
                srs_sh_ns=srs_sh_ns
            )
            session.add(create_boat)

    session.commit()
    session.close()