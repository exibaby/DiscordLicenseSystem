# ExiKeys Discord Licensing System
Welcome to ExiKeys, a Discord bot designed to manage licensing systems within your Discord server. ExiKeys allows you to generate, activate, deactivate, and check the status of licenses for your users easily.

**Installation Guide**
Follow these steps to set up ExiKeys in your Discord server:

Prerequisites
Python 3.6 or higher installed on your system.
Discord account with access to create bots and manage servers.


> 1. Clone this repository to your local machine: | git clone https://github.com/exibaby/DiscordLicenseSystem

> 2. Navigate to the project directory: | cd exikeys

> 3. Install the required Python packages using pip: | pip install -r requirements.txt

> 4. Create a new Discord bot and obtain its token. You can follow the Discord Developer Portal Guide for detailed instructions.

> 5. Replace the placeholder bot token in the code with your bot's token:

> 6. bot.run('YOUR_BOT_TOKEN_HERE')

> 7. Run the bot using Python: | python bot.py

> 8. Invite the bot to your Discord server using the OAuth2 URL generated in the Discord Developer Portal.

> 9. You're all set! Use the provided commands to manage licenses in your server.

**Features**

> License Generation: Easily generate new license keys for your users.
  
> Activation and Deactivation: Activate or deactivate licenses as needed.
  
> License Status Checking: Check the status of licenses to see if they are active.
  
> License Ownership Lookup: Find out the owner of a specific license key.

**Commands**

> /create or /generate: Generate a new license key.
  
> /activate or /use <license_key>: Activate your license.
  
> /deactivate or /stop: Deactivate your active license.
  
> /checklicense or /status: Check the status of your active license.
  
> /owner <license_key>: Check the owner of a license key.
  
> /helpsheet: Display a help sheet with all available commands and their usage.

**Support**

If you encounter any issues or have questions about ExiKeys, feel free to create an issue in this repository. You can also contact me on discord at @exibaby for further assistance.
