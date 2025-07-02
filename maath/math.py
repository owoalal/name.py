import os
import requests
from tqdm import tqdm

base_url = "https://content.plantyn.com/CMS/CDS/Plantyn/Public%20Content/Averbode/Published%20Content/Auteurs/Auteur_Franstalig/Amplitude/Tome%203/Amplitude%203%20-%20Manuel%20num%C3%A9rique%20enrichi/Resources/Amplitude3_Livrecahier_sansSolut.pdf_/"


save_folder = r"C:\Users\lomol\Downloads\math"
os.makedirs(save_folder, exist_ok=True)


cookies = {
    "_3sct": "1741958908XCASzygYT2LKEsl6pDBnvunhaL5MOW2LyaOnHpQ%2Fn%2BZyzFvVd1FFsk9zkMR65IEQOvwDs%2BrOVpkUtBZKtFoRZg1gfiG%2Bnj6F3MBj6D5MXxsPWtQO%2FX1NqzAPRvtWQwx1Y%2BMqUH4PwF1aBrXbsUEurgNrr8IrndzjWVK7MdYlUkC0UhE%3D",
    "rl_anonymous_id": "b0d2cf5e-cd23-4926-ba8b-ab72c32c4268",
    "rl_page_init_referrer": "https://www.google.com/",
    "rl_page_init_referring_domain": "www.google.com",
    "rl_user_id": "5eb73d5d-1c49-4c01-8f74-afe6014962c3",
    "rl_session": "1741958761200",
    "N@TCookie": "CDS=%7BB6052B7E%2DA7B1%2D4F66%2DA0BA%2DE939E8A7711B%7D"
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


start, end = 1,379

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
