We used a Bootstramp template to make the general layout for our website. We used a combination of css,
javascript, html and python files in order to create the website. This enabled us to better organize
our code into design, routing, and actual structuring of the website.

From our home page, we made the `map` tab route to a separate page, because that enabled us to use the Google Maps API.
We created a SQL database called `urhome.db`, so that we could have locations across the US embedded in our map. Then, we created our own resources table of the resource providers for homeless individuals in Boston. This SQL table is what feeds into our `Update` and `AddMarker` functions in `scripts.js` when we add markers to our map. 
We focused just on Boston for now, because while we initially tried to scrape the homelessness
resources from websites, we had difficulty doing so because the pages were not formatted in a consistent manner with tags that would allow for scraping and hard-coded in the markers for the few that we have now.

We also wanted the website to be able to dynamically improve without our direct input. This is why we enabled resource
providers to create accounts and log in. Using the forms on their screens, they can input comments that
would be added to the map markers. As a result, our `application.py` for our website combines many routes, for both
the user signing up, logging in and uploading content as well as those for operating the map.
