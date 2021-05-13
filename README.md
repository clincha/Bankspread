# Bankspread
### Introduction
Bankspread is a website designed to turn banking data into a spreadsheet. However, Bankspread is more of a teaching project than a production application. I wanted to take advantage of both my experience programming and my IT operations mindset. Creating an HTTPS secured website, that deploys using an automated build pipeline to cloud infrastructure would satisfy my thirst for an operational goal (the previous 4 years of university had been code heavy). 

Baillie Gifford accepted me into their 2021 IT operations graduate program cohort around the time I left university. This left months of time for me to fill in the middle of a pandemic buzzing about my new job. I began to get interested in finance and created a finance spreadsheet in Google Sheets. It listed all my accounts, stocks & shares and spending. I wanted to have it as accurate  & up to date as possible and looked into the API from Starling Bank, the bank where my account was. The resulting application, which would connect the bank to the spreadsheet, would spend the following months growing and changing. Eventually, becoming Bankspread.

### Development
Bankspread started life as a Flask Python application. I'd used Flask a few times and liked that it was written in Python, simple to set up and easy to integrate with databases. The first iterations of Bankspread (and there were many) used the personal access token to authenticate with Starling. I knew that starting small and easy and working my way up was important, previous projects had burned out quickly thanks to complex early requirements. Using Flask and personal access tokens allowed me to prototype Bankspread quickly. I had the application producing great spreadsheets in a couple of days. Using familiar technology and starting small helped me reach a working prototype fast. That prototype lit a fire that burned light during the darkest moments for the project.

[//]: # (TODO: The Starling Bank API is excellent.)

[//]: # (TODO: Learning Django)

### Operations
The continuous integration and continuous deployment tool integrated with GitHub was easy to use and has some of the best templates I've used. Setting up the pipeline was fascinating. I learned to build and upload a docker image from GitHub, how to deploy to different environments and how to embed secrets into production configuration.

AWS provided the infrastructure for Bankspread. I decided to go with IAAS because it gives me the flexibility to learn what I want, and enough interesting setup to keep it entertaining. There is a single EC2 instance with docker installed which is supporting containers that securely run Bankspread and expose it to the internet. The containers run a reverse proxy, the Bankspread Django application and a small Lets Encrypt server.

I wanted Bankspread to be accessible over HTTPS. Google sheets doesn't redirect to non-https domains and would constantly give me annoying errors. Not only that, but I was genuinely interested in learning how to properly secure websites with a certificate. Using Lets Encrypt and learning how to assign a domain to an IP address were two small but important things to learn. Being able to point a domain name to an IP address is really useful as a developer but also as an IT operations tech. It also looks really professional. Having an HTTPS certificate resolve when you hit the website so that the padlock appears just takes it up a couple of notches. Now I can do both, and this website is proof.  
