# autohome-image-spider
Spider for downloading images from autohome.

# Usage
1. (Optional) Create a virtual environment for Python:
```bash
virtualenv -p python3 spider-env
source spider-env/bin/activate
```

2. Install required Python packages:
```bash
pip3 install -r requirements.txt
···

3. Modify `misc/config,py` to custom your configuration.

4. Run script and enjoy!
```bash
scrapy crawl autohome -L "INFO"
```

- images will be download to `{IMAGE_ROOT}/{BRAND_ID}/{FCT_ID}/{SERIES_ID}/{SPEC_ID}/{IMAGE_TYPE}/{IMAGE_ID}.jpg`
