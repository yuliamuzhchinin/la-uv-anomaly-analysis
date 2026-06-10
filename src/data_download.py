"""
Data download module for LA UV Anomaly Analysis
Handles downloading DISCOVR EPIC and MERRA-2 data from NASA Earthdata

"""

import os # get NASA login
import earthaccess # download data from Earthdata
from pathlib import Path # create folders and manage file locations
import logging # track code results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EarthdataDownloader:
    def __init__ (self):
        """Initialize downloader and authenticate with Earthdata"""
        self.data_dir = Path(__file__).parent.parent / "data" / "raw"
        self.data_dir.mkdir(exist_ok=True)

        logger.info("Authenticating with Earthdata...")
        earthaccess.login(persist=True)
        logger.info("Successfully authenticated!")

    def download_data(self, collection, start_date, end_date):
        """
        Download DISCOVR EPIC UV Aerosol data
        
        Args:
            start_date: Start date (YYYY-MM-DD format, e.g., "2020-01-01")
            end_date: End date (YYYY-MM-DD format, e.g., "2026-05-31")
        
        Returns:
            List of downloaded file paths

        """

        logger.info(f"Searching for DISCOVR UV data: {start_date} to {end_date}")

        # Search Earthdata for DISCOVR EPIC UV Aresol data
        results = earthaccess.search_data(
            collection=collection,
            temporal = (start_date, end_date),
            count=100 # Get up to 199 results
        )

        logger.info(f"Found {len(results)} files")

        #Download files
        logger.info("Downloading files...")
        files = earthaccess.download(results, self.data_dir)

        logger.info(f"Downloaded {len(results)} files to {self.data_dir}")
        return files

    
def main():

    downloader =EarthdataDownloader()

    uv_files = downloader.download_data("DISCOVR_EPIC_L2_AER_03", "2020-01-01", "2026-05-31")
    print(f"UV files downloaded: {len(uv_files)}")

    aerosol_files = downloader.download_data("M2TMNXADG", "2020-01-01", "2026-05-31")
    print(f"Aerosol files downloaded: {len(aerosol_files)}")






