#/bin/bash/

src=$(pwd)


read -p "Enter the name of the User or Group's git account to be pulled: " user_group
find $src -maxdepth 1 -type d -not \( -name ".*" -prune \) -print0 | while IFS= read -rd $'\0' dir
do
	if cat .git/config |grep $user_group > /dev/null
		then
                	cd $dir
		        echo "$dir"
                        git pull
	fi
done
