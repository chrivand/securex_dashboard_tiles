# Sample script to work with SecureX Dashboard API
This is a sample script that shows the art of possible with the SecureX Dashboard API. It is meant for people who would like to create custom reports based on the SecureX dashboard tile data. This can be handy for Managed Security Services Partners (MSSP) for example.

## Overview
1. The script leverages the [SecureX Dashboard API](https://visibility.amp.cisco.com/iroh/iroh-dashboard/index.html).
2. It will grab all available tile and module information first. 
3. After this it will list all modules fot he user.
4. It will then ask if the user wants to see the tiles for a specific module.
5. After this the user is queried to see data from a specific tile.

## Installation
1. Clone this repository or download the ZIP file.
2. Log in to [https://securex.us.security.cisco.com/settings/apiClients](https://securex.us.security.cisco.com/settings/apiClients) with your Cisco Security credentials.
3. Create new API keys clicking on **Add API Credentials**.
7. Give the API Credentials a name (e.g., *Dashboard Tiles Sample Script*).
8. Select **Select All**.
9. Add an optional description if needed.
10. Click on **Add New Client**.
11. The **Client ID** and **Client Secret** are now shown to you. Do NOT click on **close** until you have copy-pasted these credentials to the config.json file in the repository.
12. Make sure that the config.json file looks like this (with the right keys and IDs filled in between the quotes):

  ```
  {
      "client_id": "<your_client_id>",
      "client_secret": "<your_client_secret>"
  }
  ```
  
14. You are now ready to execute the script. Go to a terminal and change directory to the folder that contains your **dashboard_tiles.py** and **config.json** file. 
15. Make sure you have the correct libraries installed by executing the **requirements.txt** file (use a Python virtual environment if preferred): 

  ```
  python3.8 -m venv securex_venv
  source securex_venv/bin/activate
  pip install -r requirements.txt
  ```
  
16. Now execute the **dashboard_tiles.py** script:

  ```
  python dashboard_tiles.py
  ```

17. Follow the "CLI" that the script has built in. This is pure to show you what the SecureX Dashboard API Endpoint can do. Obviously this is not that useful in production environments. When you do make your required changes, please test well before putting into production! 

## Author(s)

* Christopher van der Made - chrivand@cisco.com (Cisco)
