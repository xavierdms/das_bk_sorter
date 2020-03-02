### LICEcap GIF Walkthrough:

![alt text](https://github.com/xavierdms/das_bk_sorter/blob/master/walkthrough.gif "LICEcap GIF Walkthrough")

### Design Diary:

When this assignment was first introduced, the possibility of writing a file sorting script immediately made me think of what ended up being the final product. DAI doesn’t sort saves by character, and it also limits the saves in the game to 250. Many people’s playstyle (including mine) involves having multiple characters with 50+ (...or 100+) saves each, so having a way to sort the saves would make it easier to keep only the ones you want to play, and keep the rest in a backup location. 

At first I didn’t think I would have time to do much beyond the script itself, but I had already thought it might be cool to make an executable app with a GUI that I could share with others. I ended up finishing the script itself pretty early on, so I was able to work on the rest. I think that this tool being something I already wished existed before and wanted to use was a good motivator and why I ended up spending so much time on this assignment.

Something that was surprising (maybe because I’m not used to Python) was the fact that the pseudo code / logic of the script ended up being pretty easy to turn into actual code. The way I originally thought of each necessary step was directly translatable to code for the most part, and the fact that I didn’t expect that is probably why I thought the script would take longer to write.

The most challenging aspect was probably making the GUI itself using Qt for Python, more specifically a couple of things about it: the placement of the GUI elements, and attaching the file/directory search window to a button click. The latter ended up just needing to be its own function that gets called on click of the button. 

The backup part of it was more out of necessity since the game won’t load saves in subfolders inside the Save folder, so sorting it inside that root folder was not an option. If possible I would like to eventually add a function to delete the saves from the game folder and only keep the ones for selected characters. The current version of the app makes this easier to do than if you had to sort everything manually, but it would be cool to automate this part too.

