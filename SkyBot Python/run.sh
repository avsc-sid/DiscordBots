#!/bin/sh
set id = 0

"$HOME/SkyBot/skybotVenv/bin/activate"
python3 "$HOME/SkyBot/bot.py" &
#id=${pgrep python3}
dotnet run &

#while true;
#do
#kill $id
#sleep 21600
#git add .gitignore
#git pull <<< uncompress -c .pswd.Z
#done