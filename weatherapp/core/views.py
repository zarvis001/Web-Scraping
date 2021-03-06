from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def get_html_content(city):
    import requests
    
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city= city.replace(' ','+')
    html_content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content
    
def home(request):
    weather_data= None
    if 'city' in request.GET:
        #fatch weather data
        city= request.GET.get('city')
        html_content  =get_html_content(city)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        weather_data = dict()
        weather_data['region'] = soup.find('div', attrs={'id':'wob_loc'})
        weather_data['daytime'] = soup.find('div', attrs={'id':'wob_dts'})
        weather_data['status'] = soup.find('span', attrs={'id':'wob_dc'})
        weather_data['temp'] = soup.find('span', attrs={'id':'wob_tm'})
        
        
    
    return render(request, 'core/home.html' , {'wheather' : weather_data})