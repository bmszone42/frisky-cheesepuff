import streamlit as st
import geopy
from geopy.geocoders import Nominatim 
from fpdf import FPDF
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

# Load API key from secrets
api_key = st.secrets["MAPS_API"] 

# Set map type
map_type = 'hybrid'  

default_address = "5 Randall St, Pembroke, MA 02359"

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
    self.service = service_type
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

def update_polygon(click):
  poly.set_xy(polygon.exterior.xy)

def calculate_quote(service, area):
  if service == 'Mowing': 
    return area * 0.01
  elif service == 'Tree Trimming':
    return area * 0.05

# Core app code
selected_service = st.radio('Service', ['Mowing', 'Tree Trimming']) 

# Address input with autocomplete
address = st.text_input('Enter address', value=default_address)
lat, lon = geocode(address)

if lat is None:
  st.warning("Unable to geocode address")
else:
   
  # Geocode address
  lat, lon = geocode(address)
  
  # Generate map URL
  url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=18&size=400x400&maptype={map_type}&key={api_key}"
  
  # Display map
  st.image(url)

  # Initial polygon based on address
initial_polygon = draw_polygon([lat, lon], 0.5) 

st.write("Initial service area:", initial_polygon.area, "sq ft")

if st.button('Edit service area'):

  # Show interactive plot
  fig, ax = plt.subplots()
  poly = ax.plot(*initial_polygon.exterior.xy)

  st.pyplot(fig)

  # Callback to update polygon 
  def update(click):
    poly.set_xy(polygon.exterior.xy)  

  fig.canvas.mpl_connect('button_press_event', update)

  final_polygon = poly.get_xy()

else:
  final_polygon = initial_polygon

# Only if button clicked   
if st.button("Get Quote"):

  # Calculate price
  price = calculate_quote(service, final_polygon.area)  

  # Create quote
  quote = ServiceQuote(service, final_polygon, price)

  # Display quote
  st.header("Quote")
  st.write("Service:", quote.service)
  st.write("Area:", quote.area, "sq ft")
  st.write("Price:", quote.price)
