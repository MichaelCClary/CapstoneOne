<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** MichaelCClary, CapstoneOne, twitter_handle, MichaelCClary@gmail.com, The Vault, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/MichaelCClary/CapstoneOne">
    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
    The Vault
  </a>

  <h3 align="center">The Vault</h3>

  <p align="center">
    This is a simple website to search for new games and keep track of your games in your collection.  I hope you enjoy playing around with it as much as I did making it.  Please let me know if there are any improvements/bugs for me to make.  I plan to keep working on this to make it better and better.
    <br />
    <a href="https://github.com/MichaelCClary/CapstoneOne"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://boardgamevault.herokuapp.com/">View Demo</a>
    ·
    <a href="https://github.com/MichaelCClary/CapstoneOne/issues">Report Bug</a>
    ·
    <a href="https://github.com/MichaelCClary/CapstoneOne/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#user-flow">User Flow</a></li>
      </ul>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
I was inspired to make this project by own personal need for a way to organize my board games and to find new ones that are good.  We all have bought a game that we played once/never because it was too complicated, not fun or just not the right number of players.

This is my first capstone project with Springboard.
I built the backend with python using Flask and psql/SQLAlchemy for a database/ORM. I used Jinja, Vanilla Javascript, JQuery, and Bulma for front end.

Every search hits the api to get games and homepage is a basic search of most popular games.  When you click on more information or add a game to your collection, then it is added to the database.  

The search function was tricky because the api wouldn't let you search for say a name and a category at the same time.  It is a browse the category and search by name.  The categories/mechanics/players are in a select drop down menu for easy finding.

I used Javascript to let you add/remove games from your collection without reloading page and to handle hiding search boxes you weren't currently using.

Bulma was used to help layout the page and give me building blocks/style elements.  

Special thank you to Board Game Atlas for their API which has thousands of games to comb through.

## User Flow
1. User will go to home page
2. User can login/signup and be redirected back to homepage.
3. User can then search/browse for new games to add to their collection from taskbar
4. Any time user wants more information on a game, they just click more info button.
5. User can check their collection/profile at any time by clicking on their name from task bar
6. User can edit their information from their profile

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->
<!-- 
Here's a blank template to get started:
**To avoid retyping too much info. Do a search and replace with your text editor for the following:**
`MichaelCClary`, `CapstoneOne`, `twitter_handle`, `MichaelCClary@gmail.com`, `The Vault`, `project_description` -->


### Built With

* [Bulma](https://bulma.io/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [JQuery](jquery.com)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [PSQL](https://www.postgresql.org/)
* [Python](www.python.org)
* [bcrypt](https://pypi.org/project/bcrypt/)
* [Axios](https://github.com/axios/axios)
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Install python at python.org

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/MichaelCClary/CapstoneOne.git
   ```
2. Install requirments
   ```sh
   pip install -r requirements.txt
   ```
3. Get a free API key at https://www.boardgameatlas.com/api/docs

4. Enter your API in api_key.py
   ```sh
   client_id = 'Enter API KEY'
   ```
5. Run from terminal
   ```sh
   Flask Run
   ```


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/MichaelCClary/CapstoneOne/issues) for a list of proposed features (and known issues).

Current - high priority features
* Tags as links to that mechanic
* Improve search function
* Add favicon/vault icon
* A way to organize/reorder your collection

Some more distance features
* More than one list in collection
* Friends/friends list
* Browse other users
* Rate games
* Recommend games
* A petting zoo
* A batcave

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Email me if you have something you want me to add/a bug to fix and I will do my best.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Michael Clary - <!--[@twitter_handle](https://twitter.com/twitter_handle) --> - MichaelCClary@gmail.com

Project Link: [https://github.com/MichaelCClary/CapstoneOne](https://github.com/MichaelCClary/CapstoneOne)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Heroku](heroku.com)
* [Font Awesome](https://fontawesome.com/)
* [Board Game Atlas](https://www.boardgameatlas.com/api/docs)
* [othneildrew](https://github.com/othneildrew/Best-README-Template)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/MichaelCClary/CapstoneOne.svg?style=for-the-badge
[contributors-url]: https://github.com/MichaelCClary/CapstoneOne/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/MichaelCClary/CapstoneOne.svg?style=for-the-badge
[forks-url]: https://github.com/MichaelCClary/CapstoneOne/network/members
[stars-shield]: https://img.shields.io/github/stars/MichaelCClary/CapstoneOne.svg?style=for-the-badge
[stars-url]: https://github.com/MichaelCClary/CapstoneOne/stargazers
[issues-shield]: https://img.shields.io/github/issues/MichaelCClary/CapstoneOne.svg?style=for-the-badge
[issues-url]: https://github.com/MichaelCClary/CapstoneOne/issues
[license-shield]: https://img.shields.io/github/license/MichaelCClary/CapstoneOne.svg?style=for-the-badge
[license-url]: https://github.com/MichaelCClary/CapstoneOne/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/MichaelCClary

