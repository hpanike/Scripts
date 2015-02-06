#!/bin/bash

#Variables

PATH=$PATH:/bin/usr/bin
DATE=`date '+%F'`
DIR="<backup_dir>"
DATE2=`date '+%F %T'`

#Functions


function show_time {
    num=$1
    min=0
    hour=0
    day=0

if((num>59));then
   ((sec=num%60))
   ((num=num/60))
   if((num>59));then
      ((min=num%60))
      ((num=num/60))
      if((num>23));then
         ((hour=num%24))
	 ((day=num/24))
	 else
	    ((hour=num))
	 fi
      else
         ((min=num))
      fi
   else
      ((sec=num))
   fi
   echo "$day"d "$hour"h "$min"m "$sec"s
}	

# Get time as a UNIX timestamp (seconds elapsed since Jan 1, 1970 0:00 UTC)
T="$(date +%s)"

echo "[$DATE2:backup started]" >> /var/log/rsync.log 2>&1

if [ -e ${DIR}/3 ]; then
	TOKILL=`readlink -n ${DIR}/3`
	echo "deleting: ${DIR}/$TOKILL"
	rm -rf ${DIR}/$TOKILL && rm -rf ${DIR}/3
fi

if [ -e ${DIR}/2 ]; then
	mv ${DIR}/2 ${DIR}/3
fi

if [ -e ${DIR}/1 ]; then
	mv ${DIR}/1 ${DIR}/2
fi

if [ -e ${DIR}/0 ]; then
	mv ${DIR}/0 ${DIR}/1
fi

mkdir -p ${DIR}/$DATE

rsync -axhr --stats --safe-links --exclude-from=excludes.txt --exclude 'Trash' -z --delete \
 --link-dest=${DIR}/1/ \
 <rsync_primary_location> ${DIR}/${DATE}/ >> /var/log/rsync.log 2>&1 || echo "failed on users backup"

rsync -axhr --stats --safe-links --exclude-from=/git/backups/excludes.txt --exclude 'Trash' -z --delete \
 --link-dest=${DIR}/1/ \
 <rsync_secondary_location> ${DIR}/${DATE}/ >> /var/log/rsync.log 2>&1 || echo "failed on users backup"

 ln -s $DATE ${DIR}/0

 T="$(($(date +%s)-T))"
 echo "Backup started on: ${DATE}" >> /var/log/rsync.log 2>&1
 echo "Backup ran in: " >> /var/log/rsync.log 2>&1
 show_time  ${T} >> /var/log/rsync.log 2>&1
 printf "\n" >> /var/log/rsync.log 2>&1
 printf "\n" >> /var/log/rsync.log 2>&1
 logger "Backup ran in: ${T}. Started on ${DATE} " 
