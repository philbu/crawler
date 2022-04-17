#!/bin/bash

set -e

read -p "Enter the default directory of the project [/opt/crawler]: " app_dir
app_dir=${app_dir:-/opt/crawler}

echo "Create directory at \"$app_dir\":"
mkdir "$app_dir" && cd "$app_dir"
echo "Clone git repository:"
git clone https://github.com/philbu/crawler.git "git"
python3 -m pip install --user virtualenv && python3 -m venv env && source env/bin/activate && pip install -r git/requirements.txt

echo "Create cronjob script:"
echo "#!/bin/bash" > cronjob.sh
echo "$app_dir/env/bin/python3 -m $app_dir/git/crawler" >> cronjob.sh

echo "Next steps:"
echo "1. Add missing information to git/crawler/config.ini"
echo "2. Create a cronjob with \"crontab -e\" and add"
echo "*/5 * * * * $app_dir/git/cronjob.sh"
