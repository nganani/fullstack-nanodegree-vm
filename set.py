from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
myFirstRestaurant = Restaurant(name='Pizza Palace')
session.add(myFirstRestaurant)  # place into staging zone
session.commit()  # commit from staging zone to database
session.query(Restaurant).all()  # show all objects in table Restaurant
# cheesepizza = MenuItem(name="Cheese Pizza", description="Make with al
# natural ingridiants and fress mozzarella", course="Entree", price="$8.99",
# restaurant=firstResult)
cheesepizza = MenuItem
(name="Cheese Pizza", description="Make with all \
natural ingridiants and fress mozzarella", course="Entree", price="$8.99",
 restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()

vB = session.query(MenuItem).filter_by(name='Veggie Burger')  # filter by
