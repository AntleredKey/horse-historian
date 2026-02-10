# Horse Historian
This repo started as a simple stats calculator and historical database for LongLiveReya's Crown Prix horse game.
Reya, off the cuff, suggested having a way to run stats to offer better analyst coverage of the races, so this was made.
(I also saw it as a way to realistically showcase my Python/SQL using a fan project)

## Background
[LongLiveReya](https://www.twitch.tv/longlivereya) is a twitch streamer who saw a "Horse Race Test" game on twitter. 
The game is simple, using the same logic of a dvd-logo bouncing, but with multiple maps and horses.
Whichever horse reaches the "goal" object wins.
As a way to incentivize interaction, theres a fictional "betting" system.
Anyone with less than 1000 chips at the start of the week goes up to that maximum so they can continue betting, with no way to get more or spend chips.

Another consideration while making this was to approach this as if it was authentic horse racing / gambling. 
Having a "Since last win" to help trigger gambler's fallacy, for example.

honses.csv is the original file given to me by the Crown Prix developer, SteffanDonal - Additional races just get added to the races table, but I wanted to keep the original.
horseraces.db features the table races which is mostly just reformatted honses.csv, and horsesInRace which is it expanded for easier stats calculation.

## Scripts
### update.py
##### python3 update.py

This script updates the horsesInRace table to include new races added. It first checks if there are any new races before adding them in.

### singlehorse.py
##### python3 singlehorse.py [HORSE_CODE] <MAP_CODE>

This script runs stats for one horse, and optionally for a single map:

Races Participated
Races won
Win percentage
Since last win

### mapstats.py
##### python3 mapstats.py [MAP_CODE or ALL]

This script runs stats for maps, or optionally for every map:

Amount of races
Most wins
Highest Win Percentage
Longest Race Time
Shortest Race Time

Critically, this script doesn't handle ties. If 2+ horses have the same win percent or most wins, it only shows the first horse.

### metstats.py
##### python3 metstats.py [MAP_CODE or ALL]

This script is a joke, and just gives the same stats of mapstats.py, but with MET as if she won 100% of all races.

### racingstats.py
##### python3 racingstats.py [MAP_CODE] [g/h] [generation number or list of horses]

The best of the bunch!
This was written with the idea of "calculating stats for a race about to happen". You give it a map, and either a generation number or a list of horses.
It outputs:

Best Win Percentage
Worst Win Percentage
Most Wins
Least Wins
Most Races Participated
Longest Since Win

It also handles ties for every stat!