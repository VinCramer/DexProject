# DexProject

This is a Python project using Flask for a web-based encyclopedia for all of the creatures from the world's most popular turn-based RPG video game. Each URL ending in a valid number will display an entry consisting of a .gif and information about each monster.


Below are images showing the layout of the project:

Homepage:
![homepage](https://user-images.githubusercontent.com/32882792/45837434-54b8ed80-bcdd-11e8-822b-4fcb755c8c1c.PNG)

Search bar suggestions:
![search bar suggestions](https://user-images.githubusercontent.com/32882792/45837526-8f228a80-bcdd-11e8-808d-c30bb64b858f.PNG)
Displays all the monsters whose name contains the entered characters, in alphabetical order.

Top of dex page:
![top of dex page](https://user-images.githubusercontent.com/32882792/45837530-90ec4e00-bcdd-11e8-8b6a-90b52fc798e1.PNG)


Top of dex itself:
![top of dex](https://user-images.githubusercontent.com/32882792/45837542-95186b80-bcdd-11e8-8ce1-31ec4c381189.PNG)

Dex data:
![dex data](https://user-images.githubusercontent.com/32882792/45837551-98135c00-bcdd-11e8-8c91-73b913c52cab.PNG)
Shows abilities and hidden abilities if applicable, as well as their descriptions and some flavor text about the monster.

Dex stats:
![dex stats](https://user-images.githubusercontent.com/32882792/45837553-9a75b600-bcdd-11e8-926a-5f6f2c2c6cbe.PNG)
Stats are color coded on a scale of red=bad, yellow=ok, green=good. The width of each stat bar is based on the stat value itself.

Dex family:
![dex family](https://user-images.githubusercontent.com/32882792/45837560-9d70a680-bcdd-11e8-8c1b-011519e22960.PNG)
Shows the order of evolution from monster to monster. Each monster's image can be clicked on to be taken to their dex entry page.

All branching evolution paths are displayed in an easy to understand fashion. Below are the 2 most complex evolutionary paths for reference:

Example 1:

![branching ex 1](https://user-images.githubusercontent.com/32882792/45838182-1ae8e680-bcdf-11e8-95d3-048e294286d9.PNG)


Example 2:

![branching ex 2](https://user-images.githubusercontent.com/32882792/45838190-1e7c6d80-bcdf-11e8-8292-bfb51d82c9b8.PNG)



Dex transitions:
![dex transitions](https://user-images.githubusercontent.com/32882792/45837568-a1042d80-bcdd-11e8-8320-0b6d8a6c5df1.PNG)
Buttons at the bottom of the page to transition to the next or previous monster by number.

Type page:

![type page](https://user-images.githubusercontent.com/32882792/45837573-a5304b00-bcdd-11e8-8845-02101707d9f5.PNG)
Note that you can access the type pages by either clicking the type buttons in each dex entry, or by changing the end of the URL to a valid type

Type page links:

![type page links](https://user-images.githubusercontent.com/32882792/45837585-a8c3d200-bcdd-11e8-9fb9-947158992875.PNG)
Each name of a monster is also a link to their dex page.

404/error page:
![404](https://user-images.githubusercontent.com/32882792/45837519-8a5dd680-bcdd-11e8-9ae2-7473828fd1ad.PNG)
Displays when the user enters an invalid URL.



<a href="https://github.com/decentralion/PokemonSQLTutorial/blob/master/pokedex.sqlite">SQLite file was taken from here by GitHub user decentralion.</a>

<a href="https://github.com/fanzeyi/Pokemon-DB/blob/master/pokedex.json">JSON taken from here by GitHub user fanzeyi.</a>

<a href="https://pokemon-trainer.com/wiki/sprite-sun-moon-animated/">Main entry sprites were taken from here.</a>

<a href="https://pokemondb.net/sprites">Next/previous monster sprites on buttons were taken from here.</a>

