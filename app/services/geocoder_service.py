from app.dependencies import get_geocoder


async def get_reverse_geocode(lat: float, lon: float) -> dict:
    geocoder = await get_geocoder()
    locs_by_reverse = geocoder.reverse_geocode(lat, lon)
    return locs_by_reverse


async def get_city_by_name(name: str) -> dict:
    geocoder = await get_geocoder()
    return geocoder.geocode(name)
