# import sqlalchemy
# from sqlalchemy import create_engine, Column, Integer, String, update
# from sqlalchemy.orm import declarative_base, sessionmaker
#
# Base = declarative_base()
#
# # Create a database connection
# engine = sqlalchemy.create_engine('sqlite:///data/restaurants.sqlite')
#
# # Create a database session
# Session = sessionmaker(bind=engine)
# session = Session()
#
#
# class Restaurant(Base):
#     __tablename__ = 'restaurants'
#
#     restaurant_id = Column(Integer, primary_key=True)
#     restaurant_name = Column(String)
#     restaurant_city = Column(String)
#     famous_dish = Column(String)
#
#     def __repr__(self):
#         return f"Restaurant(restaurant_id = {self.restaurant_id}, name = {self.restaurant_name})"
#
#
# class Hotel(Base):
#     __tablename__ = 'hotels'
#
#     hotel_id = Column(Integer, primary_key=True)
#     hotel_name = Column(String)
#     hotel_city = Column(String)
#
#     def __repr__(self):
#         return f"Hotel(hotel_id = {self.hotel_id}, name = {self.hotel_name})"
#
#
# Base.metadata.create_all(engine)
#
# # restaurant = Restaurant(
# #     restaurant_id=34,
# #     restaurant_name='Taco',
# #     restaurant_city='Plainfield',
# #     famous_dish='Burrito'
# # )
# # session.add(restaurant)
# # session.commit()
#
# # hotel = Hotel(
# #     hotel_id=24,
# #     hotel_name='TA',
# #     hotel_city='Paris'
# # )
# #
# # session.add(hotel)
# # session.commit()
#
# # restaurant_to_update = session.query(Restaurant).\
# #     filter(Restaurant.restaurant_id == '33').\
# #     one()
# # restaurant_to_update.restaurant_name = 'Handi'
# # session.commit()
#
# # hotel_to_update = session.query(Hotel). \
# #     filter(Hotel.hotel_id == '22'). \
# #     one()
# # hotel_to_update.hotel_name = 'Marriott'
# # session.commit()
#
# # session.query(Restaurant).filter(Restaurant.restaurant_id==34).delete()
# # session.commit()
#
# # session.query(Hotel).filter(Hotel.hotel_id==24).delete()
# # session.commit()
#
# # restaurants = session.query(Restaurant). \
# #     order_by(Restaurant.restaurant_name.asc()). \
# #     all()
# # print(restaurants)
# #
# # for restaurant in restaurants:
# #     print(restaurant.restaurant_name, restaurant.restaurant_city)
# #
# # restaurants2 = session.query(Restaurant). \
# #     filter(Restaurant.restaurant_name == 'Mughal'). \
# #     all()
# # print(restaurants2)
# #
# # for restaurant in restaurants2:
# #     print(restaurant.restaurant_name, restaurant.restaurant_city)
#
# # hotels = session.query(Hotel). \
# #     order_by(Hotel.hotel_name.desc()). \
# #     all()
# # print(hotels)
# #
# # for hotel in hotels:
# #     print(f'Hotel name -> {hotel.hotel_name} \nHotel city -> {hotel.hotel_city}')
#
# target = 'm'.upper()
# hotels = session.query(Hotel). \
#     filter(Hotel.hotel_name.like(f'%{target}%')). \
#     all()
# print(hotels)
#
# for hotel in hotels:
#     print(f'Hotel name -> {hotel.hotel_name} \nHotel city -> {hotel.hotel_city}')