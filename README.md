# water_sort_puzzle_solver
Solver for Water Sort Puzzle App

I recently went very deep down the rabbit whole with this fun little game: [Water Sort Puzzle App](https://play.google.com/store/apps/details?id=com.gma.water.sort.puzzle&pcampaignid=web_share). However even after hours, I was unable to solve level 70.

![image](https://github.com/MPW1412/water_sort_puzzle_solver/assets/1448950/eed9281d-e83b-41a5-8366-d971966ee2d7)

Well, if you're a software developer yourself, you know what I have done. 😀

## Auto input via screenshot

Screenshot the riddle, you want to solve and save it into screenshot.jpg. Run python input_from_image.py.

https://github.com/MPW1412/water_sort_puzzle_solver/assets/1448950/f8247d3e-55c4-4c76-8dd4-1c475d258aa7

It will use object detection to parse the fluids and start the solver right away.

## Covered riddles

Use '?' as color input. The solver will run until it hits the first questionmark. You can then play the game until this point and replace the questionmark by the discovered color. Try to play around as far as you get to uncover more fields. Complete input colors as far as possible and re-run the game until all hidden fields are known.

## Manual Usage

Edit the python file to set your level and run the script.

![image](https://github.com/MPW1412/water_sort_puzzle_solver/assets/1448950/5d1959c5-de98-49b1-9724-331fa4125ad0)


