# RTimeConverter
Converts save files from different Rubiks Cube Timers.


Not close to done. 

Currently Supporting:

Ruwix.com --> 
Ruwix.com <--

Twisty Timer --> (export as BACKUP)
Twisty Timer <-- (import as BACKUP)

While trying it out, I found that Ruwiks.com sometimes doesnt accept the strings that it generated itself. Funnily, the string my program gave my after converting it to Twisty and back worked perfectly.

The reason for this is that ruwix.com sometimes adds random extra scrambles. So the string you get would i.e. contain 4 times but 5 scrambles. I assume that that is what causes the problem. My program uses the amount of available times everty time it iterates over the given data, which is why it just ignores any extra scrambles or comments. 
