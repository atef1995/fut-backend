import json
from pydantic import Json, BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import requests
from bs4 import BeautifulSoup


app = FastAPI()


class buy_now_body(BaseModel):
    amount: int
    tradeId: int
    token: str


class transfer_list(BaseModel):
    id: int
    pile: str
    token: str


AUTH_URL = r'https://www.ea.com/ea-sports-fc/ultimate-team/web-app/'

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.ea.com"
    "https://www.ea.com/*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://www.ea.com'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    external_api_url = "https://www.ea.com/ea-sports-fc/ultimate-team/web-app/config/config.json"
    external_api_url2 = "https://www.ea.com/ea-sports-fc/ultimate-team/web-app/"

    try:
        # Make the GET request to the external API
        response = requests.session().get(external_api_url)

        # Raise an exception for a bad response (status code >= 400)
        # response.raise_for_status()

        # Print the raw response content (as bytes)
        # print("Raw content:", response.content)

        # Print the response as text
        print("Text response:", response.text)

        # If the response is JSON, print the JSON response
        # print("JSON response:", response.json())

        # Print the status code of the response
        print("Status code:", response.status_code)
        print("cookies:", response.cookies)

        # Print the headers of the response
        print("Response headers:", print(
            json.dumps(dict(response.headers), indent=4)))

        # Return the JSON response (or modify this as needed)
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with external API: {str(e)}")


@app.get("/login")
async def login():
    return RedirectResponse(url=AUTH_URL)


@app.get("/callback")
async def callback(access_token: str):
    if access_token:
        return {"message": "Login successful", "access_token": access_token}
    return {"message": "error"}


@app.get("/auth")
async def auth(request: Request):
    try:
        session = requests.Session()
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,sv;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            "Host": "accounts.ea.com",
            'Origin': 'https://www.ea.com',
            'Referer': 'https://www.ea.com/',
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Dest": "",
            "Sec-Fetch-Mode": "cors",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        url = "https://accounts.ea.com/connect/auth?client_id=FUTWEB_BK_OL_SERVER&redirect_uri=nucleus:rest&response_type=code&access_token=eyJraWQiOiI4MDMwNmQ3ZS0yZjZhLTQ2MzQtYTZiMC1kNzFkZWU0YjAzYTgiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJhY2NvdW50cy5lYS5jb20iLCJqdGkiOiJTa0V4T2pJdU1Eb3hMakE2TURjME5EQm1PVFF0WmpNNU1pMDBORGMyTFdGaE1HRXROVGhpWXpNM05UUTFaRGMwIiwiYXpwIjoiRkMyNV9KU19XRUJfQVBQIiwiaWF0IjoxNzI4MDQ2Mzg3LCJleHAiOjE3MjgwNjA3ODcsInZlciI6MSwibmV4dXMiOnsicnN2ZCI6eyJlZnBsdHkiOiIxMyJ9LCJjbGkiOiJGQzI1X0pTX1dFQl9BUFAiLCJwcmQiOiIxbXB6Iiwic2NvIjoib2ZmbGluZSBkcC5pZGVudGl0eS5jbGllbnQuZXh0ZW5kZWQgc2VjdXJpdHkudHdvZmFjdG9yIGRwLmZpcnN0cGFydHljb21tZXJjZS5jbGllbnQuZXh0ZW5kZWQgc2VjdXJpdHkuY2hhbGxlbmdlIGRwLmNsaWVudC5kZWZhdWx0IHNpZ25pbiBkcC5jb21tZXJjZS5jbGllbnQuZXh0ZW5kZWQiLCJwaWQiOiIxMDAwMTk1NzczNTQ3IiwicHR5IjoiTlVDTEVVUyIsInVpZCI6IjEwMDAxOTU3NzM1NDciLCJkdmlkIjoiODJlMDkwNWMtMGU0Zi00ZWJjLWI3YzQtMTM2ZmM2NDE0NGQ2IiwicGx0eXAiOiJXRUIiLCJwbmlkIjoiRUEiLCJkcGlkIjoiV0VCIiwic3RwcyI6Ik9GRiIsInVkZyI6ZmFsc2UsImNudHkiOiIxIiwiYXVzcmMiOiIzMTQ2NTQiLCJpcGdlbyI6eyJpcCI6IjE4OC4xNTEuKi4qIiwiY3R5IjoiU0UiLCJyZWciOiJTdG9ja2hvbG0gQ291bnR5IiwiY2l0IjoiTmFja2EiLCJpc3AiOiJUZWxlMiBTd2VkZW4iLCJsYXQiOiI1OS4zMDMyIiwibGd0IjoiMTguMTU2NiIsInR6IjoiMiJ9LCJ1aWYiOnsidWRnIjpmYWxzZSwiY3R5IjoiU0UiLCJsYW4iOiJlbiIsInN0YSI6IkFDVElWRSIsImFubyI6ZmFsc2UsImFnZSI6MjksImFncCI6IkFEVUxUIn0sInBzaWYiOlt7ImlkIjo5NDAyMjIxNTYsIm5zIjoiY2VtX2VhX2lkIiwiZGlzIjoiYXRlZm05NSIsIm5pYyI6ImF0ZWZtOTUifV0sImVuYyI6IjByelhoNXRNRjIxUThFMUJnUHZWS1BOUlZaeHRtYjMraE1BMTZLK0xidlBjVytzQTJ2eDQzTC81ZFRZeG9jRjdlZXZNejUwY1ZBV0VuazlaeEtuMTFyNk1aWktQa0pYY2FvWmJvL0QzWi9LZ2h3WjlLclE3dm9pcXEvaGlBM1Z3ekVpakNZRkF0M3kvNXZGZFFKemttbzZ1c244aDlweFRHdUN5a2Jra1R3anRLb2R1aWVDdWxSUENpK1d3aUNqWE1VZFNDMFNoOHZmRmMwNEVaMzVxT0thMTJTQW9QdXBaRXUxM05FU1FuR0FHelB6dVFxRFNtRGNjTEdicnVidGY1RUFJSXhjUzFRaTdpVWROYUxSOUd0bHU0UFVSU2FITkhDOVJQMTh6YVFEYytuTll4WVlaVnk5TExKaUFrWFQrM0pVRlhPeXA5YnhEcnoyY1RRN29aK21OMVNvQytHbWxhSWU4QUV6QXJSSmRJZGVCOFNublByQ2I3eWJZWW9McG15aVE0cUN1WEdiRmwxUlgzYlFZQUJUS2dpVkl5S3k4dkVUNWJ5UkU0ZkhWenpWYmd6VUZML3lWeXphME1xNlNHTEhFTnNhcGU2MXhxZlE4b0NlK3pKeGlmWjNBMkgzT25hdHRTWHZqenp0cXd1SmU0eGIxeWJiOWprUGdPc1VYdWExREc2SzlyaHdKbDY2TzhpeU5KeGFpQWtid2ozSWttK1hGek5RM2pSM0grL2NPdWF5L2N5SGlHT3kvVHFkU1BUUzNMSHdCNUV5QUtBRXZCdzRDMVh5VUdIL0ZrQW1Zb1pncnladVFSZmV3TU9XWlR0ZHI1OEIwVmp6UzRxM3padHNtbmYwcmtPWld3cnNtT2g1Nk1sT05keVk2YVM1WUJGTWxOYUZmNVlrSW5vakpWaWwwMHBGVVUvOGtqbWF6K3REeG1tTXZOaGpkWnU2cGpuTEtsQ01Zc1Y5d3VOVXNva2svKzR6RXF4cFNIdlVjOVV4TnNsMWpwdjRMaHMrRVJ1T0NtU0dES1BDYTdsQThoeiszSVptQVhVYkozbENxY3dFOXhwL013R1BKTHQzeExKTlRTUFk3ZklFb3lOOTE4bUlvNS9kakZnSUVRa216ZGl4Rno5bVJiQ04vTFk5OExuUlJxV2luVUQzT1NyaFhYbTZkM1dMektENHE3OUducUoyc0YvbWlIVXQwUXdRemREbmpnaUt5OE5FR3RDOUs3bUxobHJPK09DalRUeHM0Qis5Vys3ZVcxaHNFd00xUlZGeDEvV3p6RjN1c2oyVmNJZThIQnNOcGN5dW53OG5VS1YvbjBCaWtlVmFxYTZ0WDkyU2gyalJjejFDR3QrN1dNV3Z2V28zenJwdXA1UHdVNEVDRlR3PT0ifX0.VzqtLzh2u7VmPPQ5kqRB-389A3FjBFudkB0ce83zS2t2GIwVDUkVeqYv165QU7JQmUMg61mi0di24HQRQ630LtlqwMfOxrnFFDLe7TOed-eX8DPz_tWUSLpZCzoE57PwdQ9QHb2fPONFphwEjzFliAk29Oy_cmNr7fTbasUSTcoPBmKGuuftK6b3Zb4T7W8sAftXqq-BkRMdiS2byd1-LkdMMRl0d7zxruMT-ySFB1WHDy0bpTh8m9cPgBHmRLBsH7hwaSbqRD_5zTZYGM14kZ8mZG252RxbfhW4d9idPb95PPe2A_uli4qC8a0fcPnioqh9H0-dYwDrUAnzPep0ew&release_type=prod&client_sequence=ut-auth"

        response = session.get(url, headers=headers)

        # Check if login was successful
        if response.status_code == 200:
            print(response.json())
            cookies = session.cookies.get_dict()
            return {"message": "Logged in successfully", "cookies": cookies}
        else:
            raise HTTPException(
                status_code=response.status_code, detail="Login failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/me")
async def me():
    url = "https://gateway.ea.com/proxy/identity/pids/me"
    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,sv;q=0.7",
        "content-type": "text/plain;charset=UTF-8",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://www.ea.com/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    try:
        response = requests.get(url, headers=headers)

        return {"res": response.json()}
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.get("/watchlist")
async def get_watchlist():
    url = 'https://utas.mob.v4.prd.futc-ext.gcp.ea.com/ut/game/fc25/watchlist'

    # Define the headers
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,sv;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'utas.mob.v4.prd.futc-ext.gcp.ea.com',
        'Origin': 'https://www.ea.com',
        'Referer': 'https://www.ea.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'X-UT-SID': 'cf8dea4e-1b0d-4912-a46e-05ab59cb6993',
        'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    try:
        response = requests.get(url, headers=headers)

        return {"res": response.json()}
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.get("/transfer-market-search")
def search_transfer_market():
    session = requests.Session()
    session.headers.update({
        'Authorization': 'Bearer eyJraWQiOiI4MDMwNmQ3ZS0yZjZhLTQ2MzQtYTZiMC1kNzFkZWU0YjAzYTgiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJhY2NvdW50cy5lYS5jb20iLCJqdGkiOiJTa0V4T2pJdU1Eb3hMakE2TURjME5EQm1PVFF0WmpNNU1pMDBORGMyTFdGaE1HRXROVGhpWXpNM05UUTFaRGMwIiwiYXpwIjoiRkMyNV9KU19XRUJfQVBQIiwiaWF0IjoxNzI4MDQ2Mzg3LCJleHAiOjE3MjgwNjA3ODcsInZlciI6MSwibmV4dXMiOnsicnN2ZCI6eyJlZnBsdHkiOiIxMyJ9LCJjbGkiOiJGQzI1X0pTX1dFQl9BUFAiLCJwcmQiOiIxbXB6Iiwic2NvIjoib2ZmbGluZSBkcC5pZGVudGl0eS5jbGllbnQuZXh0ZW5kZWQgc2VjdXJpdHkudHdvZmFjdG9yIGRwLmZpcnN0cGFydHljb21tZXJjZS5jbGllbnQuZXh0ZW5kZWQgc2VjdXJpdHkuY2hhbGxlbmdlIGRwLmNsaWVudC5kZWZhdWx0IHNpZ25pbiBkcC5jb21tZXJjZS5jbGllbnQuZXh0ZW5kZWQiLCJwaWQiOiIxMDAwMTk1NzczNTQ3IiwicHR5IjoiTlVDTEVVUyIsInVpZCI6IjEwMDAxOTU3NzM1NDciLCJkdmlkIjoiODJlMDkwNWMtMGU0Zi00ZWJjLWI3YzQtMTM2ZmM2NDE0NGQ2IiwicGx0eXAiOiJXRUIiLCJwbmlkIjoiRUEiLCJkcGlkIjoiV0VCIiwic3RwcyI6Ik9GRiIsInVkZyI6ZmFsc2UsImNudHkiOiIxIiwiYXVzcmMiOiIzMTQ2NTQiLCJpcGdlbyI6eyJpcCI6IjE4OC4xNTEuKi4qIiwiY3R5IjoiU0UiLCJyZWciOiJTdG9ja2hvbG0gQ291bnR5IiwiY2l0IjoiTmFja2EiLCJpc3AiOiJUZWxlMiBTd2VkZW4iLCJsYXQiOiI1OS4zMDMyIiwibGd0IjoiMTguMTU2NiIsInR6IjoiMiJ9LCJ1aWYiOnsidWRnIjpmYWxzZSwiY3R5IjoiU0UiLCJsYW4iOiJlbiIsInN0YSI6IkFDVElWRSIsImFubyI6ZmFsc2UsImFnZSI6MjksImFncCI6IkFEVUxUIn0sInBzaWYiOlt7ImlkIjo5NDAyMjIxNTYsIm5zIjoiY2VtX2VhX2lkIiwiZGlzIjoiYXRlZm05NSIsIm5pYyI6ImF0ZWZtOTUifV0sImVuYyI6IjByelhoNXRNRjIxUThFMUJnUHZWS1BOUlZaeHRtYjMraE1BMTZLK0xidlBjVytzQTJ2eDQzTC81ZFRZeG9jRjdlZXZNejUwY1ZBV0VuazlaeEtuMTFyNk1aWktQa0pYY2FvWmJvL0QzWi9LZ2h3WjlLclE3dm9pcXEvaGlBM1Z3ekVpakNZRkF0M3kvNXZGZFFKemttbzZ1c244aDlweFRHdUN5a2Jra1R3anRLb2R1aWVDdWxSUENpK1d3aUNqWE1VZFNDMFNoOHZmRmMwNEVaMzVxT0thMTJTQW9QdXBaRXUxM05FU1FuR0FHelB6dVFxRFNtRGNjTEdicnVidGY1RUFJSXhjUzFRaTdpVWROYUxSOUd0bHU0UFVSU2FITkhDOVJQMTh6YVFEYytuTll4WVlaVnk5TExKaUFrWFQrM0pVRlhPeXA5YnhEcnoyY1RRN29aK21OMVNvQytHbWxhSWU4QUV6QXJSSmRJZGVCOFNublByQ2I3eWJZWW9McG15aVE0cUN1WEdiRmwxUlgzYlFZQUJUS2dpVkl5S3k4dkVUNWJ5UkU0ZkhWenpWYmd6VUZML3lWeXphME1xNlNHTEhFTnNhcGU2MXhxZlE4b0NlK3pKeGlmWjNBMkgzT25hdHRTWHZqenp0cXd1SmU0eGIxeWJiOWprUGdPc1VYdWExREc2SzlyaHdKbDY2TzhpeU5KeGFpQWtid2ozSWttK1hGek5RM2pSM0grL2NPdWF5L2N5SGlHT3kvVHFkU1BUUzNMSHdCNUV5QUtBRXZCdzRDMVh5VUdIL0ZrQW1Zb1pncnladVFSZmV3TU9XWlR0ZHI1OEIwVmp6UzRxM3padHNtbmYwcmtPWld3cnNtT2g1Nk1sT05keVk2YVM1WUJGTWxOYUZmNVlrSW5vakpWaWwwMHBGVVUvOGtqbWF6K3REeG1tTXZOaGpkWnU2cGpuTEtsQ01Zc1Y5d3VOVXNva2svKzR6RXF4cFNIdlVjOVV4TnNsMWpwdjRMaHMrRVJ1T0NtU0dES1BDYTdsQThoeiszSVptQVhVYkozbENxY3dFOXhwL013R1BKTHQzeExKTlRTUFk3ZklFb3lOOTE4bUlvNS9kakZnSUVRa216ZGl4Rno5bVJiQ04vTFk5OExuUlJxV2luVUQzT1NyaFhYbTZkM1dMektENHE3OUducUoyc0YvbWlIVXQwUXdRemREbmpnaUt5OE5FR3RDOUs3bUxobHJPK09DalRUeHM0Qis5Vys3ZVcxaHNFd00xUlZGeDEvV3p6RjN1c2oyVmNJZThIQnNOcGN5dW53OG5VS1YvbjBCaWtlVmFxYTZ0WDkyU2gyalJjejFDR3QrN1dNV3Z2V28zenJwdXA1UHdVNEVDRlR3PT0ifX0.VzqtLzh2u7VmPPQ5kqRB-389A3FjBFudkB0ce83zS2t2GIwVDUkVeqYv165QU7JQmUMg61mi0di24HQRQ630LtlqwMfOxrnFFDLe7TOed-eX8DPz_tWUSLpZCzoE57PwdQ9QHb2fPONFphwEjzFliAk29Oy_cmNr7fTbasUSTcoPBmKGuuftK6b3Zb4T7W8sAftXqq-BkRMdiS2byd1-LkdMMRl0d7zxruMT-ySFB1WHDy0bpTh8m9cPgBHmRLBsH7hwaSbqRD_5zTZYGM14kZ8mZG252RxbfhW4d9idPb95PPe2A_uli4qC8a0fcPnioqh9H0-dYwDrUAnzPep0ew',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    })
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,sv;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'utas.mob.v4.prd.futc-ext.gcp.ea.com',
        'Origin': 'https://www.ea.com',
        'Referer': 'https://www.ea.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'X-UT-SID': 'c5d6081d-f27d-441c-b24c-90753b91d79e',
        'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    url = "https://utas.mob.v4.prd.futc-ext.gcp.ea.com/ut/game/fc25/transfermarket?num=21&start=0&type=player&rarityIds=0&lev=gold&leag=13&maxb=450"
    try:
        res = session.get(url, headers=headers)
        return {"res": res.json()}
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post("/buy-now")
def buy_now(request: Request, body: buy_now_body):
    buynowurl = f'https://utas.mob.v4.prd.futc-ext.gcp.ea.com/ut/game/fc25/trade/{
        body.tradeId}/bid'

    print(body)

    headers = {
        'Content-Type': 'application/json',
        'x-ut-sid': body.token,
    }
    amount = {'bid': body.amount}

    try:
        response = requests.put(buynowurl, json=amount, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(result)
            return {'res': result}
        else:
            result = response.json()
            print(type(response))
            print(result)
            return {'res': result}
    except ValueError:
        print('Response is not in JSON format:', response.text, response)
        return {'error': 'Response not in JSON format', 'content': response.text}
    except Exception as e:
        print('error', e)
        return {'error': str(e)}


@app.post('send-to-transfer-list')
def send_to_transferlist(body: transfer_list):
    url = 'https://utas.mob.v4.prd.futc-ext.gcp.ea.com/ut/game/fc25/item'

    headers = {
        'Content-Type': 'application/json',
        'x-ut-sid': body.token,
    }

    try:
        response = requests.put(url, headers=headers, json=transfer_list)

        if response == 200:
            return {'res': response.json()}
        else:
            return {'error', response.text, response.json()}
    except Exception as e:
        print(e)
        return {'error': str(e)}


@app.get('/get-player-data/{id}')
def get_player_data(id: int):

    print(id)

    url = f'https://www.fifaindex.com/player/{id}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Referer': 'https://www.fifaindex.com/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {'error', response.text, response.status_code}
        soup = BeautifulSoup(response.text, 'html.parser')
        player_name = soup.find('h5', class_='card-header')
        if player_name:
            return {'player_name': player_name.text.strip()}
        else:
            return {'error': 'player name not found'}
    except Exception as e:
        print(e)
        return {'error': str(e)}
