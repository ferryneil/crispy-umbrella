#!/bin/bash

## VARIABLES
### Your channels go here. add more channels as you want
numberofchannels=57
declare -a a0=("tvg-id-channel1" "24/7 Animaniacs" "Animaniacs" "The zany adventures of a trio of 1930s animated characters in the modern world")
declare -a a1=("tvg-id-channel2" "24/7 Asterix" "Asterix" "Asterix")
declare -a a2=("tvg-id-channel3" "24/7 Avatar" "Avatar" "Avatar")
declare -a a3=("tvg-id-channel4" "24/7 Batman The Animated Series" "Batman The Animated Series" "Batman The Animated Series")
declare -a a4=("tvg-id-channel5" "24/7 Ben 10" "Ben 10" "Ben 10")
declare -a a5=("tvg-id-channel6" "24/7 Bugs Bunny" "Bugs Bunny" "Bugs Bunny")
declare -a a6=("tvg-id-channel7" "24/7 Chip n Dale Rescue Rangers" "Chip n Dale Rescue Rangers" "Chip n Dale Rescue Rangers")
declare -a a7=("tvg-id-channel8" "24/7 Cow Chicken" "Cow & Chicken" "Cow & Chicken")
declare -a a8=("tvg-id-channel9" "24/7 Curious George" "Curious George" "Curious George")
declare -a a9=("tvg-id-channel10" "24/7 Darkwing Duck" "Darkwing Duck" "Darkwing Duck")
declare -a a10=("tvg-id-channel11" "24/7 Dinosaurs" "Dinosaurs" "Dinosaurs")
declare -a a11=("tvg-id-channel12" "24/7 Dr Seuss" "Dr Seuss" "Dr Seuss")
declare -a a12=("tvg-id-channel13" "24/7 Duck Dodgers" "Duck Dodgers" "Duck Dodgers")
declare -a a13=("tvg-id-channel14" "24/7 Duck Tales" "Duck Tales" "Duck Tales")
declare -a a14=("tvg-id-channel15" "24/7 Old DuckTales" "Old DuckTales" "Old DuckTales")
declare -a a15=("tvg-id-channel16" "24/7 Dungeons Dragons" "Dungeons & Dragons" "Dungeons & Dragons")
declare -a a16=("tvg-id-channel17" "24/7 Fairly Odd Parents" "Fairly Odd Parents" "Fairly Odd Parents")
declare -a a17=("tvg-id-channel18" "24/7 Fireman Sam" "Fireman Sam" "Fireman Sam")
declare -a a18=("tvg-id-channel19" "24/7 Fraggle Rock" "Fraggle Rock" "Fraggle Rock")
declare -a a19=("tvg-id-channel20" "24/7 He-Man" "He-Man" "He-Man")
declare -a a20=("tvg-id-channel21" "24/7 Horrid Henry" "Horrid Henry" "Horrid Henry")
declare -a a21=("tvg-id-channel22" "24/7 Inspector Gadget" "Inspector Gadget" "Inspector Gadget")
declare -a a22=("tvg-id-channel23" "24/7 Lego Star Wars" "Lego Star Wars" "Lego Star Wars")
declare -a a23=("tvg-id-channel24" "24/7 Looney Tunes" "Looney Tunes" "Looney Tunes")
declare -a a24=("tvg-id-channel25" "24/7 Mickey Mouse" "Mickey Mouse" "Mickey Mouse")
declare -a a25=("tvg-id-channel26" "24/7 Mr Bean Animated Series" "Mr Bean Animated Series" "Mr Bean Animated Series")
declare -a a26=("tvg-id-channel27" "24/7 Muppet Babies" "Muppet Babies" "Muppet Babies")
declare -a a27=("tvg-id-channel28" "24/7 Pinky and The Brain" "Pinky and The Brain" "Pinky and The Brain")
declare -a a28=("tvg-id-channel29" "24/7 Pokemon" "Pokemon" "Pokemon")
declare -a a29=("tvg-id-channel30" "24/7 Popeye" "Popeye" "Popeye")
declare -a a30=("tvg-id-channel31" "24/7 Rugrats" "Rugrats" "Rugrats")
declare -a a31=("tvg-id-channel32" "24/7 Rugrats All Grown Up" "Rugrats All Grown Up" "Rugrats All Grown Up")
declare -a a32=("tvg-id-channel33" "24/7 Scooby-Doo" "Scooby-Doo" "Scooby-Doo")
declare -a a33=("tvg-id-channel34" "24/7 Spider-Man Animated" "Spider-Man Animated" "Spider-Man Animated")
declare -a a34=("tvg-id-channel35" "24/7 Star Wars Rebels" "Star Wars Rebels" "Star Wars Rebels")
declare -a a35=("tvg-id-channel36" "24/7 Stingray" "Stingray" "Stingray")
declare -a a36=("tvg-id-channel37" "24/7 Street Sharks" "Street Sharks" "Street Sharks")
declare -a a37=("tvg-id-channel38" "24/7 Super Mario Bros" "Super Mario Bros" "Super Mario Bros")
declare -a a38=("tvg-id-channel39" "24/7 Teen Titans Go" "Teen Titans Go" "Teen Titans Go")
declare -a a39=("tvg-id-channel40" "24/7 Teenage Mutant Ninja Turtles" "Teenage Mutant Ninja Turtles" "Teenage Mutant Ninja Turtles")
declare -a a40=("tvg-id-channel41" "24/7 The Amazing World of Gumball" "The Amazing World of Gumball" "The Amazing World of Gumball")
declare -a a41=("tvg-id-channel42" "24/7 The Banana Splits" "The Banana Splits" "The Banana Splits")
declare -a a42=("tvg-id-channel43" "24/7 The Flintstones" "The Flintstones" "The Flintstones")
declare -a a43=("tvg-id-channel44" "24/7 The Jetsons" "The Jetsons" "The Jetsons")
declare -a a44=("tvg-id-channel45" "24/7 The Loud House" "The Loud House" "The Loud House")
declare -a a45=("tvg-id-channel46" "24/7 The Muppet Show" "The Muppet Show" "The Muppet Show")
declare -a a46=("tvg-id-channel47" "24/7 The Racoons" "The Racoons" "The Racoons")
declare -a a47=("tvg-id-channel48" "24/7 The Real Ghostbusters" "The Real Ghostbusters" "The Real Ghostbusters")
declare -a a48=("tvg-id-channel49" "24/7 The Pink Panther Show" "The Pink Panther Show" "The Pink Panther Show")
declare -a a49=("tvg-id-channel50" "24/7 Thomas and Friends" "Thomas and Friends" "Thomas and Friends")
declare -a a50=("tvg-id-channel51" "24/7 Thunderbirds Are Go" "Thunderbirds Are Go" "Thunderbirds Are Go")
declare -a a51=("tvg-id-channel52" "24/7 Thundercats" "Thundercats" "Thundercats")
declare -a a52=("tvg-id-channel53" "24/7 Tom and Jerry" "Tom and Jerry" "Tom and Jerry")
declare -a a53=("tvg-id-channel54" "24/7 Top Cat" "Top Cat" "Top Cat")
declare -a a54=("tvg-id-channel55" "24/7 Transformers Prime" "Transformers Prime" "Transformers Prime")
declare -a a55=("tvg-id-channel56" "24/7 Transformers Rescue Bots" "Transformers Rescue Bots" "Transformers Rescue Bots")
declare -a a56=("tvg-id-channel57" "24/7 X-Men Animated" "X-Men Animated" "X-Men Animated")

starttimes=("000000" "010000" "020000" "030000" "040000" "050000" "060000" "070000" "080000" "090000" "100000" "110000" "120000" "130000" "140000" "150000" "160000" "170000" "180000" "190000" "200000" "210000" "220000" "230000") 
endtimes=("010000" "020000" "030000" "040000" "050000" "060000" "070000" "080000" "090000" "100000" "110000" "120000" "130000" "140000" "150000" "160000" "170000" "180000" "190000" "200000" "210000" "220000" "230000"  "235900")
BASEPATH="/users/neil/webgrab/wg++/dummyepgxml-main"
DUMMYFILENAME=dummy.xml

		today=$(date "+%Y%m%d")
		tomorrow=$(date  --date="tomorrow" "+%Y%m%d")
		echo '<?xml version="1.0" encoding="UTF-8"?>' > $BASEPATH/$DUMMYFILENAME
		echo '<tv generator-info-name="mydummy" generator-info-url="https://null.null/">' >> $BASEPATH/$DUMMYFILENAME
        numberofiterations=$(($numberofchannels - 1))
        echo "Creating Dummy Epg ..."


		for i in $(seq 0 $numberofiterations); do # Number of Dummys -1 
			tvgid=a$i[0]
			name=a$i[1]
			echo '    <channel id="'${!tvgid}'">' >> $BASEPATH/$DUMMYFILENAME
			echo '        <display-name lang="en">'${!name}'</display-name>' >> $BASEPATH/$DUMMYFILENAME
			echo '    </channel>' >> $BASEPATH/$DUMMYFILENAME
		done

		for i in $(seq 0 $numberofiterations) ;do
			tvgid=a$i[0]
			title=a$i[2]
			desc=a$i[3]
			for j in {0..23}; do
					echo '    <programme start="'$today${starttimes[$j]}' +0000" stop="'$today${endtimes[$j]}' +0000" channel="'${!tvgid}'">' >> $BASEPATH/$DUMMYFILENAME
					echo '        <title lang="en">'${!title}'</title>' >> $BASEPATH/$DUMMYFILENAME
					echo '        <desc lang="en">'${!desc}'</desc>' >> $BASEPATH/$DUMMYFILENAME
					echo '    </programme>' >> $BASEPATH/$DUMMYFILENAME
			done
			for j in {0..23}; do
					echo '    <programme start="'$tomorrow${starttimes[$j]}' +0000" stop="'$tomorrow${endtimes[$j]}' +0000" channel="'${!tvgid}'">' >> $BASEPATH/$DUMMYFILENAME
					echo '        <title lang="en">'${!title}'</title>' >> $BASEPATH/$DUMMYFILENAME
					echo '        <desc lang="en">'${!desc}'</desc>' >> $BASEPATH/$DUMMYFILENAME
					echo '    </programme>' >> $BASEPATH/$DUMMYFILENAME
			done
		done

		echo '</tv>' >> $BASEPATH/$DUMMYFILENAME

echo "Done!"
sleep 2
