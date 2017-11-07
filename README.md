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
2. Extract the [zip archive][zip] to the `Packages` directory, rename it to `Writing Style`, and delete the zip archive  
3. Restart Sublime Text

How Can I Configure What gets Highlighted?
------------------------------------------
Create (or open) a file called ```SublimeWritingStyle.sublime-settings``` in your Packages/User directory.
For instance, you can add extra weasel words using the ```extra_words``` key or overwrite existing weasel words using the ```weasel_words``` key.
You can enable the plugin on additional file types using the ```extra_extensions``` key.

How Can I Adjust the Colors of the Highlights?
-----------------------------------------------
The icons come in dark and light versions. You can switch this by adding this to your user settings:

```json
"theme": "light"
```

Valid theme values are: `light`, `dark`, and `none`. The last option turns off gutter icons.


Add this to your theme, and adjust the colors as necessary:

```xml
<!-- Support for SublimeWritingStyle -->
<dict>
    <key>name</key>
    <string>SublimeWritingStyle.Passive</string>
    <key>scope</key>
    <string>writingstyle.passive</string>
    <key>settings</key>
    <dict>
        <key>foreground</key>
        <string>#40BFFF</string>
    </dict>
</dict>
<dict>
    <key>name</key>
    <string>SublimeWritingStyle.Weasel</string>
    <key>scope</key>
    <string>writingstyle.weasel</string>
    <key>settings</key>
    <dict>
        <key>foreground</key>
        <string>#E09500</string>
    </dict>
</dict>
```


Who Inspired This Package?
--------------------------

[Stefan Brunthaler](http://www.ics.uci.edu/~sbruntha/) extended the [writegood-mode](https://github.com/bnbeckwith/writegood-mode) for [Emacs](http://www.gnu.org/software/emacs/) in a similar fashion.

Icons made by [Freepik][2] from [www.flaticon.com][3] is licensed by [Creative Commons BY 3.0][4]

 [0]: https://sublime.wbond.net/
 [1]: https://sublime.wbond.net/installation
 [2]: http://www.freepik.com
 [3]: http://www.flaticon.com
 [4]: http://creativecommons.org/licenses/by/3.0/
 [zip]: https://github.com/thedataking/SublimeWritingStyle/archive/master.zip
