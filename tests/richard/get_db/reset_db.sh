#!/bin/bash -xe

# things to do to make this work:
# ssh-copy-id pyvideo.org
# rsync dump_x.sh pyvideo.org:
# ./manage.py syncdb --migrate
# ./manage.py dumpdata auth > auth.json

# instance is a dir/site/db on pyvideo.org
# carl@stark:~$ ls /srv
# flourish  pyvideo  test_pyvideo

instance=dev_pyvideo

source /home/carl/.virtualenvs/richard/bin/activate 

# dump data from db to file on remote filesystem
ssh pyvideo.org ./dump_x.sh $instance

# pull that file to local filesystem
rsync -vP pyvideo.org:richard_${instance}_videos.json .

# blow away and reset previous local database
mv database.db ~/temp/ || /bin/true
python ./manage.py syncdb --migrate --noinput
# ./manage.py load_sampledata

# load data from remote
python ./manage.py loaddata richard_${instance}_videos.json

# load user/pw from local static 
python ./manage.py loaddata auth.json

# run local server
./runsrv.sh
