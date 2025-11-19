from dotenv import load_dotenv
import os
from imagekitio import ImageKit

load_dotenv()

imagekit = ImageKit(
    private_key=os.getenv("IMAGE_PRIVATE_KEY"),
    public_key=os.getenv("IMAGE_PUBLIC_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL")
)

