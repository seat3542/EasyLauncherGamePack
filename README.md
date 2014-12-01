<h3>EASY LAUNCHER GAME PACK</h3>
<h4>originally created by littlefiredragon & seat3542</h4>
<p>Readme Last Updated: Dec 1 2014</p>

<h4>Description</h4>
<p>Easy Launcher Game Pack is, as its name suggests, an easy-to-use launcher
system for various open source games. Feel free to contribute a game under
a GNU GPL-compatible license.</p>

<h4>Dependencies</h4>
<ul>
<li>tkinter</li>
</ul>

<h4>How to Build the Code</h4>

<h4>How to Run the Launcher</h4>


<h4>How to Add a Game</h4>


<h4>Rules of Contribution</h4>
<h5>Licence</h5>
<p>This project is licensed under GNU GPL. All components must be compatible
with the GPL license. Graphics and other arts included are licensed as
Creative Commons Attribution-Noncommercial-Sharealike.</p>

<h5>Bug Reports</h5>
<h6>Claiming a Bug</h6>
<p>Bugs are to be reported through github issues and an issue is to be 
claimed before resolving it. If an issue has been claimed but the one who
claimed it has neither resolved it nor reported any progress via comments
on the issue page within four weeks of claiming it, it is assumed that
they have abandoned it and the bug is free to be claimed by someone else.</p>
<h6>Submitting a Bug</h6>
<p>The first line of a bug report should indicate where the bug occurs:
either the game it is part of, or that it occurs in the launcher. There should
be a section labeled BUG TRIGGERS which describes what causes the bug to occur; 
essentially, instructions on how to reproduce the error. Be sure to include 
the situation and player input (if applicable) that cause the bug. There should 
also be a section called DESCRIPTION that describes what the bug actually does.</p>
<h6>Sample Bug Report</h6>
```
BATTLESHIP
BUG TRIGGERS:
Player attacks vertically oriented enemy sloop. Bug appears to occur 
regardless of what other ships have been hit/sunk by the player and 
by the computer. Bug appears to be unrelated to the number of turns 
taken, or position/orientation of player's ships. Bug does not occur
with horizontally oriented enemy sloop.
DESCRIPTION:
Red X appears correctly on the map. Fire does not appear on player's
map, but player's own sloop takes damage as indicated by the damage
meter. This damage can sink the player's ship.
```

<h5>Pull Requests</h5>
1. A pull request that only adds a new game and does not change the 
   other files in any other way needs only 1 positive review.
2. Extremely minor edits like fixing a typo need no reviews and can be
   accepted by their own creator.
3. Larger edits that change already-existing files beyond merely adding
   a new game to the launcher must get 3 positive reviews or an okay from
   littlefiredragon or seat3542. If a pull request gets 3 negative reviews
   it is to be rejected.


<h5>Coding Standards</h5>
<p>ALL languages must have function descriptions. </p>

* PYTHON: http://legacy.python.org/dev/peps/pep-0008/ 
* C: 
 * General style: http://users.ece.cmu.edu/~eno/coding/CCodingStandard.html 
 * Allman Bracketing: http://en.wikipedia.org/wiki/Indent_style#Allman_style 
 * functionNamesLikeThis 
 * Function header style: 

        ```C
        /****************************************************************************
         * Function:     functionName
         * Description:  Description goes here.
         *               Additional lines like this.
         * Parameters:   parameter1  -  explanation
         *               param2      -  explanation
         * Returns:      returnvalue -  explanation                
         ***************************************************************************/
        double functionName (int parameter1, char param2)
        // Function code happens down here
        ```
        
* C++: http://www.possibility.com/Cpp/CppCodingStandard.html 
* JAVA: 
<p>If you use a language not yet listed, please add it to this list.</p>

<h5>Testing</h5>
<p>All programs should be functional and complete before being added to the launcher. We expect they have been tested for major bugs. It should be ready for release. As such we have no policy on unittesting or anything of that nature, as there should be only minor bugs at worst. <br />
This project has been tested on:  </p>
<ul>
<li>openSUSE 13.1 64 bit</li>
</ul>
