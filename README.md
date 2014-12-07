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
<li>Python 3</li>
</ul>

<h4>How to Build the Code</h4>

<h4>How to Run the Launcher</h4>


<h4>How to Add a Game</h4>
<p>To add a game, simply edit Buttons.txt. Place your game on a new line with
the following format: 
Name of your button;File path to your game;Name of executable;Name of About File;
*Note*
Make sure each piece of information on the line is seperated by a semicolon as
shown above. There should be NO spaces before and after the semicolons. Make sure to
end each line with a semicolon. Incorrect formatting can result in file paths not 
being found and would not allow your game to launch successfully. The file path to
your game is simply where your executable is located. Name of execuatable must include
relevant extensions (.py for python, .cpp for c++, etc.) and the about file should
be in standard .txt format. Here's an example within our own project:

BattleShip;battleship;battleship.py;DEFAULT.txt;

If you do not have an About file, please use DEFAULT.txt. Do not leave that portion
blank. Note that the above file path would look different for code written in java.
For example java code might look like the following:

BattleShip;battleship/src;battleship.py;DEFAULT.txt;

Do not place a blank line at the bottom of the file.Please follow the format exactly 
when contributing to the project, otherwise it will result in a bug. 

<h4>Rules of Contribution</h4>
<h5>Licence</h5>
<p>This project is licensed under GNU GPL. All components must be compatible
with the GPL license. Graphics and other arts included are licensed as
Creative Commons Attribution-Noncommercial-Sharealike. Attribution can be in
the game or in the game's description file. As this is an open source project,
should any part of the project containing creative commons licensed media be
reused elsewhere without also reusing the part containing the attribution, the 
reused part in question must be modified to contain the attribution.</p>

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
<h6>Example Bug Report</h6>
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
   other files in any other way needs only 1 positive review. This
   review is to be given by someone who has tested the submitted game to
   determine that it is functional and playable. Rule of thumb:
   Would you commercially release a game in this state of completion? If
   so, the game is playable and functional, and therefore fit for release.
2. Extremely minor edits like fixing a typo need no reviews and can be
   accepted by their own creator.
3. Larger edits that change already-existing files beyond merely adding
   a new game to the launcher must get 3 positive reviews or an okay from
   littlefiredragon or seat3542. If a pull request gets 3 negative reviews
   it is to be rejected. Positive reviews are not to be given without at
   the very least carefully reading the new code, and preferably not given
   without testing the code.
4. Feature requests are to be submitted on Github Issues. The first line
   of the issue should indicate what game it is for, or that it is for the
   launcher. If it gets 3 positive reviews or an okay from littlefiredragon
   or seat3542, the feature request is considered open for claiming.
   Claiming a feature request functions identically to claiming a bug.
   Submitting a feature request is optional; one can simply make a pull
   request with the modification already in place, and it will be subject
   to Pull Request Rule 3 as normal.


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
* JAVA: http://www.oracle.com/technetwork/java/codeconvtoc-136057.html
<p>If you use a language not yet listed, please add it to this list.</p>

<h5>Testing</h5>
<p>All programs should be functional and complete before being added to the launcher. We expect they have been tested for major bugs. These games should be ready for release. As such we have no standard policy on unittesting or anything of that nature, as there should be only minor bugs at worst. <br />
This project has been tested on:  </p>
<ul>
<li>openSUSE 13.1 64 bit</li>
</ul>
