SublimeWritingStyle
===================

Improve your writing style with this Sublime Text package. 
It supports both Sublime Text 2 and 3.

Why Should I Write in Style?
------------------------------

Practicing your writing skills will make you a more effective communicator.

How Does This Package Help Me?
-----------------------------------

It does two things. First, it helps you use *active voice* instead of *passive voice*.
Consider these two sentences:

- The car was driven by the boy. 

- The boy drove the car.

Which one is simpler? (Hint, it's the second, active one.) Using active voice simultaneously makes your text shorter and more engaging to the reader. Unfortunately, it takes some practice to spot passive sentences. 
Passive voice indicators are forms of *to be* (am, is, are, was, were, be, been, being) plus another verb (often ending in *ed*).

Second, this package highlights *weasel words*. Use these judgmental words sparingly. A few examples: *very, clearly, and, relatively*. 

Both the list of passive voice indicators and weasel words are customizable using Sublime Text settings files.  Use the `extra_words` settings key to define additional highlighted words.

How to Install
------------------------------------------

#### Using [Package Control][0] (Recommended):

1. [Install][1] Package Control
2. Open the command palette (`cmd+shift+P`) then `Package Control: Install Package`
3. Search for `Writing Style`
4. (Optionally) Reopen any windows

#### Manually:

1. Open the `Preferences > Browse Packages…` menu
2. Browse up a folder and then into the `Installed Packages/` folder
3. Download [zip archive][zip] rename it to `SublimeWritingStyle.sublime-package` and copy it into the `Installed Packages/` directory
4. Restart Sublime Text

How Can I Configure What gets Highlighted?
------------------------------------------
Create (or open) a file called ```SublimeWritingStyle.sublime-settings``` in your Packages/User directory.
For instance, you can add extra weasel words using the ```extra_words``` key or overwrite existing weasel words using the ```weasel_words``` key.
You can enable the plugin on additional file types using the ```extra_extensions``` key.

Who Inspired This Package?
--------------------------

[Stefan Brunthaler](http://www.ics.uci.edu/~sbruntha/) extended the [writegood-mode](https://github.com/bnbeckwith/writegood-mode) for [Emacs](http://www.gnu.org/software/emacs/) in a similar fashion.

 [0]: https://sublime.wbond.net/
 [1]: https://sublime.wbond.net/installation
 [zip]: https://github.com/revolunet/sublimetext-markdown-preview/archive/master.zip