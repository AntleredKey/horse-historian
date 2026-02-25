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

In the past_csv dir, there is honses1.csv which served as the basis of this project. It was given to me by the Crown Prix developer, SteffanDonal - Additional races just get added to the races table, but I wanted to keep the original.
honses2.csv was a later addition.
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

### weekly.py
##### python3 weekly.py [YYYY-MM-DD]

This creates a weekly.txt file for Crown Pix Weekly Winners. It outputs every race from that date (including that date) to present because I couldn't figure out weeks, and if there was a world record time.

YYYY-MM-DD - [horse_code] with a time of [duration] on [map], <'WORLD RECORD!!' if WR>

## Program

Named in files as App.py this is an attempt to merge the above scripts into a single program with a GUI.

### List

This, functionally, just merges mapstats.py and singlehorse.py but they were reworked to accept more than just "one map or all maps".

### Compare

This is an expansion on racingstats.py ... Previously, racingstats.py only accepted a single map and with 2+ horses, but this expansion allows 0 to 3 maps and 0 to 12 horses (with some resulting in errors). There was an attempt to make things intuitive and for as little errors as possible to be thrown, but you can't really "compare" a single horse.