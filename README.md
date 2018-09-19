# PyTab

I couldn't find a simple, free software to type and display guitar tablature, so I made one with curses.

## Requirements
Requires Python 3.6+ for string interpolation but could be modified to work with older versions. No dependencies other than standard library.
## Tab object
The module includes the `Tab` object, which is basically just some data fields and a method to open a curses display for editing

All arguments are optional, and are listed below
- `title`: string for song title
- `artist`: string for artist name
- `tuning`: string representing open notes
- `capo`: integer for capo fret number
- `n`: integer for number of notes to put in a measure
- `m`: integer for maximum measures to put in one row (will display fewer than this if the screen is not wide enough)

Controls in the curses display:
- q: quit the display
- o: save the file
- arrow keys or wasd: move the cursor
- 0-9, h, p, /, -, x: enters the chosen character into the display at the cursor location
- insert: inserts a new row at the bottom of the file. throws an error if going off the bottom of the screen

### Example
```python
# create a new Tab
tab = Tab(title="Even The Darkness Has Arms", artist="The Barr Brothers", tuning='DGDGBD', n=16, m=2)

# open the curses display and write to the tab
tab.edit()
```

This will open a display that looks like this

```
Even The Darkness Has Arms - The Barr Brothers
Tuning: D G D G B D

D|--------------------------------|--------------------------------|
B|--------------------------------|--------------------------------|
G|--------------------------------|--------------------------------|
D|--------------------------------|--------------------------------|
G|--------------------------------|--------------------------------|
D|--------------------------------|--------------------------------|
```

###### future features:
- scrolling at bottom of screen for longer tabs
- ask to confirm exit if the file has not been saved
- allow for reopening a tab to edit again
- load a saved tab
