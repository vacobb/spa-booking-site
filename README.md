# Day Spa Service Booking - Webapp
#### Video Demo:  <URL [HERE](https://youtu.be/04ebjzS3Qns)>
#### Description:

**/register**

Starting with the registration page. This page has a simple form that allows the user to create an account. It has fields for first and last name, username, and a password. There are conditions set so that all fields have to be filled in in order to submit the form. If the user leaves a field empty, they are shown an error that prompts them to fill it in before submitting. Also, there is a password confirmation field to make sure that the user did not mistype their password.

**/login**

Once the user has created their account, they can log in to the website with their unique username and password.

**/index**

After logging in, the user is shown a variety of things on the index page. They page has an area that shows a snippet of their account information, a place to book services, and a section that displays the services that have been booked. The area that shows the account information shows the most important information (name, profile pic, and year they established membership) to be sure the right user has been logged in.

The main function of the page is to book appointments and display booked services. On the righthand side, there are 3 dropdowns that allow the user to choose a service, as well as a day and time for that service. Once they have made their selection, there is a button that submits their selection. After selecting a service, it shows up in their "Booked Services" table on the left. The use has the ability to cancel any service, but clicking the X button on the "Booked Services" table.

If the user tries to book a day/time combo that is already taken, the site will flash a warning that they have to choose a different apointment day/time combo. The "Booked Services" table is also set to display all services they have chosen in chronological order.

**/account**

This page is meant to allow users to update their account information. They can change their name and upload a new profile picture. It also displays the year they joined the site, this is not able to be updated as it should not ever be debated or changed. The name and photo can be updated seperately and do not need to be updated at the same time. The account information on the /index page is sourced from this page.

**/layout**

This page sets up the general layout that is mirrored on every page of the website. It's where the navigation bar, with all of its buttons and logo photo at the top of the page are housed. I even added the functionality of highlighting the name of the page that you are on, so that it stands out from the other links in the navigation bar. It also houses the necessary links to make the Bootstrap code work.

**spa.db**

This file holds the 2 databases that make my website run.

The first is the 'users' database. It contains the user's user id, username, name, password (hashed), and file path for their profile picture. This database supports the functionality that allows you to create a profile, log in, and navigate the website.

The second is 'services'. This one houses all of the information that supports the "Booked Services" table.

**styles.css**

This file holds some CSS code to help stylize my page. Specifically, it holds code to deal with the navigation bar, table properties, and profile pictures. The navigation bar and table properties come form Bootstrap. However, the profile picture style tags are my own and meant to make the profile picture small with rounded corners.

**app.py**

This file has all of my Python coding as well as the JavaScript that makes the HTML and JavaScript work together. This is where a lot of the processing of information happens. There are a number of nested loops and conditional clauses that direct the function of each choice the user makes on their end.

**helpers.py**

This files specifically holds the code needed to keep users logged in to my website until they are logged out.
# spa-booking-site
