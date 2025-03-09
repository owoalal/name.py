import os
import requests
from tqdm import tqdm

base_url = "https://content.plantyn.com/CMS/CDS/Plantyn/Public%20Content/Averbode/Published%20Content/Auteurs/Auteur_Franstalig/Amplitude/Tome%203/Amplitude%203%20-%20R%C3%A9f%C3%A9rentiel/Resources/Amplitude3_Referentiel.pdf_/"


save_folder = r"C:\Users\lomol\Downloads\math"
os.makedirs(save_folder, exist_ok=True)


cookies = {
    "_3sct": "1741458172XCASJFpd8uXUWdpbN5WRq6LZMwvsXQyTPU631D55Hf4CvC8BrHK%2BYpdiKTsEGuxwSStMFJEtPOtR5a%2FyfH49lAr1YCj1wHLG%2F7Jm%2FmpS1u6nWRci%2F85K3wsDov98OSjOu8n6RCvt6r1U7kyVz8geavdo52y1%2Frb5y0MWifVCJyuyFcA%3D",
    "rl_anonymous_id": "b0d2cf5e-cd23-4926-ba8b-ab72c32c4268",
    "rl_page_init_referrer": "https://www.google.com/",
    "rl_page_init_referring_domain": "www.google.com",
    "rl_user_id": "5eb73d5d-1c49-4c01-8f74-afe6014962c3",
    "rl_session": "1741457333617",
    "N@TCookie": "CDS=%7B30C5DF0B%2DB785%2D42CD%2DA383%2D850A2A18DF7E%7D"
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


start, end = 1,99

for i in tqdm(range(start, end + 1), desc="Downloading images"):
    img_url = f"{base_url}{i}.png"
    img_path = os.path.join(save_folder, f"{i}.png")

    try:
        response = requests.get(img_url, headers=headers, cookies=cookies, stream=True)
        if response.status_code == 200:
            with open(img_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        else:
            print(f"Failed to download {img_url} (Status: {response.status_code})")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

print(f"Download completed! Images saved in '{save_folder}'")
