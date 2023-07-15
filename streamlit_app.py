import streamlit as st
import geopy
from geopy.geocoders import Nominatim 
from fpdf import FPDF
from shapely.geometry import Polygon

class User:
  def __init__(self, name, email):
    self.name = name
    self.email = email

class ServiceArea:
  def __init__(self, address, polygon, size):
    self.address = address
    self.polygon = polygon
    self.size = size

class ServiceQuote:
  def __init__(self, service_type, area, price):
    self.service_type = service_type
    self.area = area
    self.price = price

  def generate_pdf(self):
    pdf = FPDF() 
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Service Quote')
    pdf.output('quote.pdf')

# Helper functions

def geocode(address):

  geolocator = Nominatim(user_agent="app")
  location = geolocator.geocode(address)

  if location is None:
    print("Unable to geocode address")
    return None, None
  
  return location.latitude, location.longitude

def draw_polygon(center, size):
  polygon = Polygon([(center[0]-size, center[1]-size), 
                     (center[0]+size, center[1]-size),
                     (center[0]+size, center[1]+size),
                     (center[0]-size, center[1]+size)])
  return polygon

def calculate_quote(service, area):
  if service == 'Mowing': 
    return area * 0.01
  elif service == 'Tree Trimming':
    return area * 0.05

# Core app code

selected_service = st.radio('Service', ['Mowing', 'Tree Trimming']) 

address = st.text_input('Address')
lat, lon = geocode(address)

if lat is None:
  st.warning("Unable to geocode address")
else:
  # Create map, polygon, etc

polygon = draw_polygon([lat, lon], 0.5) 

quote = ServiceQuote(selected_service, polygon, calculate_quote(selected_service, polygon.area))

st.write("Your quote is:", quote.price)

if st.button('Email Quote'):
  quote.generate_pdf()
