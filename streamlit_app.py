import streamlit as st
import geopy
from geopy.geocoders import Nominatim 
from fpdf import FPDF
from shapely.geometry import Polygon

# Load API key from secrets
api_key = st.secrets["MAPS_API"] 

# Set map type
map_type = 'hybrid'  

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

# Address input with autocomplete
address = st.text_input('Enter address', autocomplete='on')

lat, lon = geocode(address)

if lat is None:
  st.warning("Unable to geocode address")
else:
  # Create map, polygon, etc
   
  # Geocode address
  lat, lon = geocode(address)
  

  # Generate map URL
  url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=18&size=400x400&maptype={map_type}&key={api_key}"
  
  # Display map
  st.image(url)

  # After geocoding
  polygon = draw_polygon([lat, lon], 0.5) 
  
  # Create quote
  quote = ServiceQuote(selected_service, polygon, price) 
  
  # Display quote details
  st.subheader("Quote Summary")
  st.write("Service Type:", quote.service)
  st.write("Area:", quote.area, "sq. ft")  
  st.write("Price:", quote.price)
