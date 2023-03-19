# Typing Spped Test
#### Video Demo: https://youtu.be/P--NDKFmUjU
#### Distinctiveness and Complexity:
* Real-time performance assessment: application works in real time, so it requires additional logic that exceeds the complexity of previously used.
* Custom typing tests: user has an ability to create custom texts, that complicates the managing of the data.
* Ranking: this section of the web application requires a lot of back-end development, since, as mentioned in the previous paragraph, it's at least 2 different rankings for each type of texts. 
* Results calculations: all the data are being gathered simultaneously as the user uses the app, which is a drastically distinct from every other project's background implementation, where all the data was gathered after submitting the forms, clicking buttons etc. 
* User authentication and authorization: event though it's no new concepts here, it's a gender selection by registration, that is responsible for the avatar in a profile page. This sort of influence from a registration data wasn't implemented in the previous projects.
* Multiple views and templates: this is neither new, nor distinctive concept from all other projects, but it meets all requirements of the final project, as it has a bunch of views and templates, as well as 3 django models for user, custom text, and result
* Handling various request methods: the app utilizes all the features of HTTP request, since it uses redirecting to another pages through the links, GETing and POSTing data using fetch function in js.
---
In summary it provides a customizable typing test environment with a real-time ranking system. It tracks user performance and saves their scores, displaying their ranking among other users. Additionally, the application fetches random texts from an external API, providing a unique typing experience for each test.
#### Description:
Typing Speed Test is an engaging and interactive web application designed to help users improve their typing skills by offering real-time performance assessments, as well as some custom content, and a competitive ranking system.

Upon registration, users gain access to a range of features, including custom typing tests, where they can create their own content or choose from existing. As users are completing tests, the app tracks their words-per-minute, characters-per-minute, and accuracy rates, displaying all the information after the timer goes off.

The app is also offering a ranking system that sorts users based on their typing performance that makes competitive environment. Users can view their rankings and compare their results with others in both standard and custom test modes.

Built with security and user experience in mind, this app implements user authentication and authorization, ensuring that each user's data is stored separately and securely. The app also employs AJAX and JSON to enable smooth interactions and seamless data exchange without the need for full page reloads.

Overall, Typing Speed Test is an entertaining web app that combines learning and competition, offering users an enjoyable way to enhance their typing skills.

##### More on files:

###### Static:

* Index.js: this js file is responsible for loading all the data we see on the screen. It fetches random text using API and then loads it to a textarea form. It also tracks spelled and misspelled letters in order to calculate chars/min and accuracy at the end. Word's implemented through increasing its value every time space occurs to be in the text. It also cleans a text from all excessive symbols and allow only alphabetical and digits. It's an event listener that helps to always keep a focus on the textarea, which is invisible, but helps a lot to collect an input. After the timer goes off, it runs a fetch function to post results and save it to the database(but only if users click on the "save result" button).
* Custom.js: basically does the same as index.js, except it uses additional fetch request to get a custom text, and then display it.

###### Templates:

* layout.html: it's a base of every used html page, contains nav bar with all the links.
* index.html: an html for the main page, contains 2 sections (test and results) that index.js toggles between.
* login.html, register.html: default login and register pages, except the register page takes into an account a gender, that is responsible for the profile's avatar
* custom.html: similar to the index.html, but contains 1 more section, custom text selection. It provides a list of all the posted texts, and a search bar so that the user can easily find suitable text.
* profile.html: contains a user's card with a pfp and an amount of completed tests. Behind the card is a top 3 results of the user.
* ranking.html: contains 2 sections: standard and custom. In a standard section are all the scores gathered from API's texts, in a custom - from custom texts. If the user is not logged in, he can't access custom texts ranking.
* text_form.html: a form for creating a custom text, can be accessed only by authenticated users. It requires a title so it could be found Custom section, and a text area that should be filled with at least 1000 characters, since it's nearly the world record for speed typing in one minute interval.
  
###### Views

* It starts with a default login, register, and logout views. All the other functions are mainly for interacting with js fetch function, since I tried to make it as asynchronous as possible. But still there are a few functions for rendering pages with some input parameters.
  

###### How to launch it:
In order to use the program, no additional modules or frameworks except Django are required. The only thing needed is an API key for a WikiHow. It can be retrieved on this website for free: https://rapidapi.com/hargrimm/api/wikihow/
After completing registration, the API key for can be accessed without any problems.
Then, clone this repository and run the server in the terminal.