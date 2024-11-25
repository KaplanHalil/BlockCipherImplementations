Kaynak : https://www.freecodecamp.org/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/

#bash scripts end with .sh

***************************************
#Bash critpler shebang ile başlar 

#! /usr/bin/bash
***************************************
#You can find your bash shell path  using the command:

which bash
***
#To access the variable value, append $ to the variable name.

country=Pakistan
echo $country
new_country = $country
echo $new_country

***
We can read the user input using the read command.

#!/bin/bash 

echo "What's your name?" 

read entered_name 

echo -e "\nWelcome to bash tutorial" $entered_name

***

This code reads each line from a file named input.txt and prints it to the terminal. 

#!/bin/bash 
while read line
do
  echo $line
done < input.txt

***

$1 fonksiyonu çağırıken ilk verdiğimiz girdiyi $2 ikinciyi vb ifade eder.

***
if/else
Syntax:
if [[ condition ]];
then
   	statement
elif [[ condition ]]; then
    statement 
else
    do this by default
fi
We can use logical operators such as AND -a and OR -o to make comparisons that have more significance: 

if [ $a -gt 60 -a $b -lt 100 ]

#!/bin/bash

echo "Please enter a number: "
read num

if [ $num -gt 0 ]; then
  echo "$num is positive"

elif [ $num -lt 0 ]; then
  echo "$num is negative"
else
  echo "$num is zero"
fi

***
while:

#!/bin/bash
i=1
while [[ $i -le 10 ]] ; do
   echo "$i"
  (( i += 1 ))
done

***
for:

#!/bin/bash
for i in {1..5}
do
    echo $i
done

***************************************
case:

fruit="apple"

case $fruit in
    "apple")
        echo "This is a red fruit."
        ;;
    "banana")
        echo "This is a yellow fruit."
        ;;
    "orange")
        echo "This is an orange fruit."
        ;;
    *)
        echo "Unknown fruit."
        ;;
esac