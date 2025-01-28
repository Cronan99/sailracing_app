from app import create_app
from srs_scrape import create_boat_objects


app = create_app()

if __name__=="__main__":
    create_boat_objects()
    app.run(debug=True)