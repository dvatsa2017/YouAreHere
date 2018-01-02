We used a Bootstramp template to make the general template for our website. We used a combination of css,
javascript, html and python files in order to create the website. This enabled us to better organize
our code into design, routing, and actual structuring of the website.

From our home page, we made the map tab route to a separate page, because that enabled us to adapt our map from the mashup problem set.
We created a SQL database called urhome.db and took the places table from mashup.db, so that we could have the locations
across the US embedded in our map. We initally tried to embed the map within the landing page. However, certain functionalities of the map from mashup were difficult to consolidate in index.html. Then, we created our own resources table of the resource providers for
homeless individuals in Boston. This SQL table is what feeds into our Update and AddMarker functions in scripts.js when we add markers
to our map. While the original mashup problem set restricts to 10 items per field of view, we felt
that this restriction doesn't make sense when wanting to see resources in one's area so we got rid of this
restriction. We focused just on Boston for now, because while we initially tried to scrape the homelessness
resources from websites, we had difficulty doing so because the pages were not formatted in a consistent manner with tags that would allow for scraping and hard-coded in the markers for the few that we have now.

We also wanted the website to be able to dynamically improve without our direct input. This is why we enabled resource
providers to create accounts and log in. Using the forms on their screens, they can input comments that
would be added to the map markers. As such, in addition to building off of mashup, we also built off the
finance problem set. As a result, our application.py for our website combines many routes, for both
the user signing up, logging in and uploading content as well as those for operating the map.